# E-Commerce Backend Application

## Overview
A FastAPI-based backend for an e-commerce platform, implementing APIs for managing products and orders with MongoDB.

The application includes the following key features:
- **Product Management**: Create and list products with details like name, price, and available sizes.
- **Order Management**: Create orders with user ID and item details (product ID and quantity), and list orders with enriched product information and totals.
- **Pagination**: Supports paginated responses for the list endpoints.
- **Validation**: Uses Pydantic for request and response validation with positive value constraints.

## Tech Stack
- Python 3.12
- FastAPI
- MongoDB (Pymongo)
- python-dotenv
- Deployed on Render

## Installation

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd TaskBackend
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install fastapi uvicorn pydantic pymongo
   ```

4. **Configure MongoDB**
   - Ensure MongoDB is running locally (default port 27017) or update `database.py` with your MongoDB connection string.
   - Example `database.py`:
     ```python
     from pymongo import MongoClient

     client = MongoClient("mongodb://localhost:27017/")
     db = client["taskBackend_db"]
     products_collection = db["products"]
     orders_collection = db["orders"]
     ```

5. **Run the Application**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   - Access the interactive API documentation at `http://localhost:8000/docs`.

## Project Structure

```
Task_backend/
│
├── database.py         # MongoDB connection and collection definitions
├── main.py             # FastAPI application with API endpoints
├── models.py           # Pydantic models for request and response validation
└── README.md           # This file
```

### **File Details**

- **`database.py`**
  - Defines the MongoDB client and collections (`products_collection`, `orders_collection`).
  - Assumes a local MongoDB instance; modify the connection string for remote use.

- **`main.py`**
  - Contains the FastAPI app with four endpoints:
    - `POST /products`: Creates a new product.
    - `GET /products`: Lists products with optional filters and pagination.
    - `POST /orders`: Creates a new order with user ID and items.
    - `GET /orders/{user_id}`: Lists orders for a user with pagination and enriched item details.
  - Uses Pydantic models for input/output validation and MongoDB for data storage.

- **`models.py`**
  - Defines Pydantic models for all API requests and responses:
    - `SizeItem`: Represents size and quantity for products.
    - `ProductCreate`: Schema for creating products.
    - `ProductResponse`: Response for a created product.
    - `ProductListItem`: Item in the product list response.
    - `ProductDetails`: Nested object for order item product details.
    - `OrderItem`: Schema for order items with product details and quantity.
    - `OrderCreate`: Schema for creating orders.
    - `OrderResponse`: Response for a created order.
    - `OrderListItem`: Item in the order list response.
    - `Pagination`: Pagination metadata.
    - `ProductListResponse`: Response for listing products.
    - `OrderListResponse`: Response for listing orders.

## API Endpoints

### **1. Create Product**
- **Endpoint**: `POST /products`
- **Request Body**:
  ```json
  {
    "name": "Tablet",
    "price": 5000.0,
    "sizes": [
      {"size": "M", "quantity": 10},
      {"size": "L", "quantity": 5}
    ]
  }
  ```
- **Response**: `201 Created`
  ```json
  {
    "id": "some_mongo_id"
  }
  ```

### **2. List Products**
- **Endpoint**: `GET /products`
- **Query Parameters**:
  - `name` (optional): Filter by product name.
  - `size` (optional): Filter by size.
  - `limit` (default: 10): Number of items per page.
  - `offset` (default: 0): Offset for pagination.
- **Response**: `200 OK`
  ```json
  {
    "data": [
      {
        "id": "687e214383c7b73ddb932c92",
        "name": "Tablet",
        "price": 5000.0,
        "sizes": [
          {"size": "M", "quantity": 10},
          {"size": "L", "quantity": 5}
        ]
      }
    ],
    "page": {
      "next": null,
      "limit": 10,
      "previous": null
    }
  }
  ```

### **3. Create Order**
- **Endpoint**: `POST /orders`
- **Request Body**:
  ```json
  {
    "userId": "Mukhtar",
    "items": [
      {
        "productId": "687e214383c7b73ddb932c92",
        "qty": 1
      },
      {
        "productId": "687e218783c7b73ddb932c93",
        "qty": 3
      }
    ]
  }
  ```
- **Response**: `201 Created`
  ```json
  {
    "id": "some_mongo_id"
  }
  ```
- **Note**: `productId` must exist in the `products` collection, or a 400 error is returned.

### **4. List Orders**
- **Endpoint**: `GET /orders/{user_id}`
- **Path Parameter**: `user_id` (e.g., "Mukhtar")
- **Query Parameters**:
  - `limit` (default: 10): Number of items per page.
  - `offset` (default: 0): Offset for pagination.
- **Response**: `200 OK`
  ```json
  {
    "data": [
      {
        "id": "687e29faa5e9b8352c1ece6e",
        "userId": "Mukhtar",
        "items": [
          {
            "productDetails": {
              "productId": "687e214383c7b73ddb932c92",
              "name": "Tablet"
            },
            "qty": 1
          },
          {
            "productDetails": {
              "productId": "687e218783c7b73ddb932c93",
              "name": "Phone"
            },
            "qty": 3
          }
        ],
        "total": 9500
      }
    ],
    "page": {
      "next": null,
      "limit": 10,
      "previous": null
    },
    "total": 9500
  }
  ```
- **Note**: `total` is the sum of `qty * price` per order, and the root `total` is the sum of all order totals.

## Debugging

- If endpoints return unexpected results (e.g., empty `data` in `GET /orders/{user_id}`):
  - Check the terminal for debug output (`Orders count`).
  - Verify data in the `orders` and `products` collections.
  - Ensure `productId` values in orders match `_id` values in products.

## Deployment

1. Deploy to a platform like Render:
   - Set up a new web service.
   - Use the repository URL and the command `uvicorn main:app --host 0.0.0.0 --port $PORT`.
   - Provide the MongoDB connection string as an environment variable.
2. Submit the base URL (e.g., `https://your-app.onrender.com`)