# main.py

from fastapi import FastAPI, HTTPException, Depends, status
from .models import (
    ProductModel,
    CoinModel,
    SelectProductModel,
    InsertCoinModel,
    VendResponseModel,
    LoadChangeModel,
    LoadProductsModel,
    VendRequestModel,
)
from .product import Product
from .coin import COIN_DENOMINATIONS
from .database import products_db, change_db
from typing import Dict, Optional
import uuid

app = FastAPI(
    title="Vending Machine API",
    description="An API for a vending machine that handles product selection, coin insertion, and vending.",
    version="1.0.0",
)

# Session data to keep track of user transactions
session_data: Dict[str, Dict] = {}

# Dependency to get session data
def get_session(session_id: str):
    if session_id not in session_data:
        session_data[session_id] = {
            "current_amount": 0,
            "selected_product": None,
        }
    return session_data[session_id]

@app.post("/load_products", response_model=Dict[str, str])
def load_products(products: Dict[str, ProductModel]):
    """
    Load products into the vending machine.
    """
    for product in products.values():
        if product.name in products_db:
            products_db[product.name].quantity += product.quantity
        else:
            products_db[product.name] = Product(product.name, product.price, product.quantity)
    return {"status": "Products loaded successfully"}

@app.get("/products", response_model=Dict[str, ProductModel])
def get_products():
    """
    Get the list of products.
    """
    return {name: ProductModel(name=prod.name, price=prod.price, quantity=prod.quantity) for name, prod in products_db.items()}

@app.post("/load_change", response_model=Dict[str, str])
def load_change(coins: LoadChangeModel):
    """
    Load change into the vending machine.
    """
    for denomination in coins.coins.keys():
        if denomination not in COIN_DENOMINATIONS:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Invalid coin denomination: {denomination}")
    for denomination, quantity in coins.coins.items():    
        change_db[denomination] += quantity
    return {"status": "Change loaded successfully"}


@app.get("/change", response_model=Dict[int, int])
def get_change():
    """
    Get the current state of the change in the vending machine.

    Returns:
        A dictionary mapping coin denominations to their quantities.
    """
    return change_db.copy()

@app.post("/start_session", response_model=Dict[str, str])
def start_session():
    """
    Start a new vending machine session.
    """
    session_id = str(uuid.uuid4())
    session_data[session_id] = {
        "current_amount": 0,
        "selected_product": None,
    }
    return {"session_id": session_id}

@app.post("/select_product", response_model=Dict[str, str])
def select_product(select_product: SelectProductModel, session_id: str):
    """
    Select a product.
    """
    session = get_session(session_id)
    product_name = select_product.product_name
    if product_name in products_db and products_db[product_name].quantity > 0:
        session["selected_product"] = products_db[product_name]
        return {"status": f"Product {product_name} selected"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not available or out of stock")

@app.post("/insert_coin", response_model=Dict[str, str])
def insert_coin(coin: InsertCoinModel, session_id: str):
    """
    Insert a coin.
    """
    session = get_session(session_id)
    denomination = coin.coin
    if denomination not in COIN_DENOMINATIONS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid coin denomination")
    session["current_amount"] += denomination
    change_db[denomination] += 1  # Machine keeps the coin
    return {"status": f"Inserted {denomination}p"}

@app.post("/vend", response_model=VendResponseModel)
def vend(session_id: str):
    """
    Attempt to vend the selected product.
    """
    session = get_session(session_id)
    selected_product: Optional[Product] = session.get("selected_product")
    current_amount: int = session.get("current_amount", 0)

    if selected_product is None:
        return VendResponseModel(success=False, message="No product selected")

    if current_amount < selected_product.price:
        required = selected_product.price - current_amount
        return VendResponseModel(success=False, message=f"Insufficient funds. Please insert {required}p more.")

    if products_db[selected_product.name].quantity <= 0:
        return VendResponseModel(success=False, message="Product out of stock")

    # Calculate change
    change_to_return = current_amount - selected_product.price
    change_given = calculate_change(change_to_return)
    if change_given is None:
        return VendResponseModel(success=False, message="Unable to provide change")

    # Update product quantity
    products_db[selected_product.name].quantity -= 1

    # Update change - remove coins given as change
    for coin, quantity in change_given.items():
        change_db[coin] -= quantity

    # Reset session data
    session["current_amount"] = 0
    session["selected_product"] = None

    change_str = format_change(change_given)
    message = f"Dispensed {selected_product.name}"
    if change_str:
        message += f", Change given: {change_str}"
    return VendResponseModel(success=True, message=message)

@app.post("/reset_session", response_model=Dict[str, str])
def reset_session(session_id: str):
    """
    Reset the current session. Return any money left
    """
    left_amount = 0
    if session_id in session_data:
        session = session_data[session_id]
        left_amount = session.get("current_amount", 0)
        del session_data[session_id]
    change_given = calculate_change(left_amount)  # we don't need to check if it's none, because this scenario happens when money added and cancelled, so for sure we have the change
    # Update change - remove coins given as change
    for coin, quantity in change_given.items():
        change_db[coin] -= quantity
    change_str = format_change(change_given)
    message = f"Session reset successfully"
    if change_str:
        message += f", Change given: {change_str}"
    return {"status": message}

def calculate_change(amount: int) -> Optional[Dict[int, int]]:
    """
    Calculate change to return to the customer.

    :param amount: Amount of change to return in pennies.
    :return: Dictionary mapping coin denominations to quantities, or None if change cannot be made.
    """
    change_given = {}
    amount_left = amount
    # Sort coins in descending order
    for coin in sorted(change_db.keys(), reverse=True):
        coin_quantity = change_db[coin]
        if coin <= amount_left and coin_quantity > 0:
            num_coins = min(amount_left // coin, coin_quantity)
            if num_coins > 0:
                change_given[coin] = num_coins
                amount_left -= coin * num_coins
    if amount_left == 0:
        return change_given
    else:
        return None

def format_change(change: Dict[int, int]) -> str:
    """
    Format change dictionary into a string.

    :param change: Dictionary mapping coin denominations to quantities.
    :return: String representation of the change.
    """
    parts = []
    for coin, quantity in sorted(change.items(), reverse=True):
        coin_value = f"£{coin // 100}" if coin >= 100 else f"{coin}p"
        parts.append(f"{quantity} x {coin_value}")
    return ", ".join(parts)