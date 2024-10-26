# cli.py

import uuid
import main as vm
from product import Product
from coin import COIN_DENOMINATIONS

def display_menu():
    print("\nWelcome to the Vending Machine!")
    print("Please choose an option:")
    print("1. Load Products")
    print("2. Load Change")
    print("3. View Products")
    print("4. Select Product")
    print("5. Insert Coin")
    print("6. Vend")
    print("7. View Change Status")
    print("8. Reset Transaction")
    print("9. Exit")

def main():
    session_id = str(uuid.uuid4())
    print(f"Session ID: {session_id}")
    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            # Load Products
            num_products = int(input("Enter number of products to load: "))
            products = []
            for _ in range(num_products):
                name = input("Product name: ")
                price = int(input("Product price (in pennies): "))
                quantity = int(input("Product quantity: "))
                products.append(Product(name, price, quantity))
            vm.load_products(products)
            print("Products loaded successfully.")
        elif choice == '2':
            # Load Change
            print("Available denominations: ", COIN_DENOMINATIONS)
            num_coins = int(input("Enter number of coin types to load: "))
            coins = {}
            for _ in range(num_coins):
                denomination = int(input("Coin denomination (in pennies): "))
                if denomination not in COIN_DENOMINATIONS:
                    print(f"Invalid denomination: {denomination}")
                    continue
                quantity = int(input("Coin quantity: "))
                coins[denomination] = quantity
            vm.load_change(coins)
            print("Change loaded successfully.")
        elif choice == '3':
            # View Products
            products = vm.get_product_list()
            if products:
                print("\nAvailable Products:")
                for product in products:
                    print(product)
            else:
                print("No products available.")
        elif choice == '4':
            # Select Product
            product_name = input("Enter product name to select: ")
            success = vm.select_product(product_name)
            if success:
                print(f"Product '{product_name}' selected.")
            else:
                print(f"Product '{product_name}' not available.")
        elif choice == '5':
            # Insert Coin
            denomination = int(input("Enter coin denomination (in pennies): "))
            success = vm.insert_coin(denomination)
            if success:
                print(f"Inserted {denomination}p.")
            else:
                print("Invalid coin denomination.")
        elif choice == '6':
            # Vend
            success, message = vm.vend()
            print(message)
        elif choice == '7':
            # View Change Status
            change_status = vm.get_change_state()
            if change_status:
                print("\nCurrent Change Status:")
                for denomination, quantity in sorted(change_status.items()):
                    coin_value = f"£{denomination // 100}" if denomination >= 100 else f"{denomination}p"
                    print(f"{coin_value}: {quantity}")
            else:
                print("No change available.")
        elif choice == '8':
            # Reset Transaction
            vm.reset_transaction()
            print("Transaction reset successfully.")
        elif choice == '9':
            # Exit
            print("Thank you for using the Vending Machine. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()