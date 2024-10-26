# tests/test_main.py

import unittest
from fastapi.testclient import TestClient
from main import app

class TestVendingMachineAPI(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)

    def test_load_products(self):
        response = self.client.post("/load_products", json={
                "Soda": {"name": "Soda", "price": 125, "quantity": 10},
                "Chips": {"name": "Chips", "price": 75, "quantity": 5}
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Products loaded successfully", response.json()["status"])

    def test_load_change(self):
        response = self.client.post("/load_change", json={
            "coins": { "50": 20, "100": 10 }
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Change loaded successfully", response.json()["status"])

    def test_vending_flow(self):
        # Start a session
        response = self.client.post("/start_session")
        self.assertEqual(response.status_code, 200)
        session_id = response.json()["session_id"]

        # Load products and change
        self.client.post("/load_products", json={
                "Water": {"name": "Water", "price": 100, "quantity": 10}
        })
        self.client.post("/load_change", json={
            "coins": { "50": 10, "20": 10, "10": 10 }
        })

        # Select product
        response = self.client.post("/select_product", params={"session_id": session_id}, json={
            "product_name": "Water"
        })
        self.assertEqual(response.status_code, 200)

        # Insert coin
        response = self.client.post("/insert_coin", params={"session_id": session_id}, json={
            "coin": 100
        })
        self.assertEqual(response.status_code, 200)

        # Vend
        response = self.client.post("/vend", params={"session_id": session_id})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["success"])
        self.assertIn("Dispensed Water", response.json()["message"])

    def test_insufficient_funds(self):
        # Start a session
        response = self.client.post("/start_session")
        session_id = response.json()["session_id"]

        # Load products
        self.client.post("/load_products", json={
                "Juice": {"name": "Juice", "price": 150, "quantity": 5}
        })

        # Select product
        self.client.post("/select_product", params={"session_id": session_id}, json={
            "product_name": "Juice"
        })

        # Insert coin
        self.client.post("/insert_coin", params={"session_id": session_id}, json={
            "coin": 100
        })

        # Attempt to vend
        response = self.client.post("/vend", params={"session_id": session_id})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["success"])
        self.assertIn("Insufficient funds", response.json()["message"])

    def test_invalid_coin(self):
        # Start a session
        response = self.client.post("/start_session")
        session_id = response.json()["session_id"]

        # Attempt to insert invalid coin
        response = self.client.post("/insert_coin", params={"session_id": session_id}, json={
            "coin": 3
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid coin denomination", response.json()["detail"])

    def test_product_out_of_stock(self):
        # Start a session
        response = self.client.post("/start_session")
        session_id = response.json()["session_id"]

        # Load products
        self.client.post("/load_products", json={
            "products": {
                "Candy": {"name": "Candy", "price": 60, "quantity": 1}
            }
        })

        # Select product
        self.client.post("/select_product", params={"session_id": session_id}, json={
            "product_name": "Candy"
        })

        # Insert coins
        self.client.post("/insert_coin", params={"session_id": session_id}, json={
            "coin": 100
        })

        # Vend
        self.client.post("/vend", params={"session_id": session_id})

        # Try to purchase again
        response = self.client.post("/select_product", params={"session_id": session_id}, json={
            "product_name": "Candy"
        })
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product not available or out of stock", response.json()["detail"])

    def test_reset_session(self):
        # Start a session
        response = self.client.post("/start_session")
        session_id = response.json()["session_id"]

        # Reset session
        response = self.client.post("/reset_session", params={"session_id": session_id})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Session reset successfully", response.json()["status"])

if __name__ == '__main__':
    unittest.main()