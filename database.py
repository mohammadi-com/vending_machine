# database.py

from typing import Dict
from product import Product
from coin import COIN_DENOMINATIONS

# In-memory data store
products_db: Dict[str, Product] = {}
change_db: Dict[int, int] = {denomination: 0 for denomination in COIN_DENOMINATIONS}