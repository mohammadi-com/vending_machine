# product.py

class Product:
    """
    Class representing a product in the vending machine.
    """

    def __init__(self, name: str, price: int, quantity: int):
        """
        Initialize a product.

        :param name: Name of the product.
        :param price: Price of the product in pennies.
        :param quantity: Quantity of the product in stock.
        """
        self.name = name
        self.price = price  # in pennies
        self.quantity = quantity

    def __str__(self):
        return f"{self.name} - Price: {self.price}p, Quantity: {self.quantity}"