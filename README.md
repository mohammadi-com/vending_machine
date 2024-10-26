# Vending Machine

An interactive vending machine implemented in Python using FastAPI. The application simulates a vending machine that allows users to select products, insert coins, and receive products along with appropriate change. It supports loading products and change, resetting sessions, and viewing the current state of products and change.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
    - [Running the API Server](#running-the-api-server)
    - [Interactive API Documentation](#interactive-api-documentation)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Examples](#examples)
- [Using the API with curl](#using-the-api-with-curl)
- [Notes](#notes)

## Features

- **Product Management**: Load and view available products in the vending machine.
- **Change Management**: Load and view the current state of change in the machine.
- **Session Management**: Start, reset, and manage sessions for individual users.
- **Transaction Handling**: Select products, insert coins, vend items, and receive change.
- **Error Handling**: Provides informative error messages for invalid inputs and actions.
- **Testing**: Comprehensive test suite to ensure all functionalities work as expected.
- **Command-Line Interface**: Interact with the vending machine via a CLI for demonstration purposes.

## Project Structure
```
vending_machine/
├── __init__.py
├── coin.py              # Defines coin denominations
├── product.py           # Defines the Product class
├── main.py              # FastAPI application
├── models.py            # Pydantic models for API
├── database.py          # In-memory data store
└── tests/
    ├── __init__.py
    └── test_main.py     # Tests for API endpoints
```

## Installation

### Prerequisites

- Python 3.7 or higher
- pip package manager

### Install Dependencies

Navigate to the project directory and install the required packages:

```
pip install -r requirements.txt
```

## Usage

### Running the API Server

#### Navigate to the Project Directory
```
cd vending_machine
```

#### Start the Server

Run the FastAPI application:
```
uvicorn main:app --reload
```

#### Access the API
The API will be available at http://127.0.0.1:8000.

## Interactive API Documentation

FastAPI provides interactive documentation powered by Swagger UI. Access it at:

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Interact with the Vending Machine
Follow the on-screen prompts to load products, insert coins, select products, and vend items.

## API Endpoints

- POST /load_products: Load products into the vending machine.
- POST /load_change: Load change into the vending machine.
- GET /products: Retrieve a list of available products.
- GET /change: Retrieve the current state of change in the machine.
- POST /start_session: Start a new vending machine session.
- POST /select_product: Select a product for purchase.
- POST /insert_coin: Insert a coin into the machine.
- POST /vend: Attempt to vend the selected product.
- POST /reset_session: Reset the current session and return any inserted money.

## Testing

A comprehensive test suite is provided to ensure all functionalities work as expected.

Running the Tests

Navigate to the project directory and execute:
```
python -m unittest discover -s tests
```
All tests should pass, confirming that the application is functioning correctly.

## Examples

### Using the API with curl

Start a Session
```
curl -X POST http://127.0.0.1:8000/start_session
```
Response:
```
{
  "session_id": "your-generated-session-id"
}
```
Load Products
```
curl -X POST http://127.0.0.1:8000/load_products \
  -H "Content-Type: application/json" \
  -d '{
        "products": {
          "Water": {"name": "Water", "price": 100, "quantity": 20},
          "Juice": {"name": "Juice", "price": 150, "quantity": 15}
        }
      }'
```
Load Change
```
curl -X POST http://127.0.0.1:8000/load_change \
  -H "Content-Type: application/json" \
  -d '{
        "coins": {
          "10": 50,
          "20": 50,
          "50": 50,
          "100": 50
        }
      }'
```
Select Product
```
curl -X POST "http://127.0.0.1:8000/select_product?session_id=your-session-id" \
  -H "Content-Type: application/json" \
  -d '{ "product_name": "Water" }'
```
Insert Coin
```
curl -X POST "http://127.0.0.1:8000/insert_coin?session_id=your-session-id" \
  -H "Content-Type: application/json" \
  -d '{ "coin": 100 }'
```
Vend
```
curl -X POST "http://127.0.0.1:8000/vend?session_id=your-session-id"
```
Response:
```
{
  "success": true,
  "message": "Dispensed Water"
}
```
Reset Session
```
curl -X POST "http://127.0.0.1:8000/reset_session?session_id=your-session-id"
```
Response:
```
{
  "status": "Session reset successfully. Returned 0p"
}
```

## Notes

- Data Persistence: The application uses in-memory data stores (products_db, change_db, session_data). All data will reset when the application is stopped. In a production environment, a persistent database should be used.
- Session Management: Each user interaction is tracked via a session_id to simulate individual user sessions.
- Coin Denominations: Valid coin denominations are 1p, 2p, 5p, 10p, 20p, 50p, £1 (100p), and £2 (200p).
- Error Handling: The API and CLI handle invalid inputs gracefully, providing informative error messages without crashing.
- Thread Safety: In a production environment, consider thread safety and concurrency issues, especially if deploying with multiple workers.

Thank you for using the Vending Machine API!