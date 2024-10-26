# models.py

from pydantic import BaseModel
from typing import Optional, Dict

class ProductModel(BaseModel):
    name: str
    price: int  # in pennies
    quantity: int

class CoinModel(BaseModel):
    denomination: int
    quantity: int

class SelectProductModel(BaseModel):
    product_name: str

class InsertCoinModel(BaseModel):
    coin: int  # denomination in pennies

class VendResponseModel(BaseModel):
    success: bool
    message: str

class LoadChangeModel(BaseModel):
    coins: Dict[int, int]  # denomination to quantity

class LoadProductsModel(BaseModel):
    products: Dict[str, int]  # product name to quantity

class VendRequestModel(BaseModel):
    session_id: str