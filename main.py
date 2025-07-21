from fastapi import FastAPI, HTTPException
from models import ProductCreate, ProductResponse, OrderCreate, OrderResponse, ProductListResponse, OrderListResponse, SizeItem, OrderItem, Pagination, ProductListItem, OrderListItem, ProductDetails
from database import products_collection, orders_collection
from typing import List, Optional
from bson.objectid import ObjectId  # Explicit import for ObjectId
from datetime import datetime

app = FastAPI()

def objectid_to_str(obj):
    if isinstance(obj, ObjectId):
        return str(obj)
    return obj

@app.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    product_dict = product.dict()
    result = products_collection.insert_one(product_dict)
    return {"id": str(result.inserted_id)}

@app.get("/products", response_model=ProductListResponse)
async def list_products(name: Optional[str] = None, size: Optional[str] = None, limit: int = 10, offset: int = 0):
    query = {}
    if name:
        query["name"] = {"$regex": name, "$options": "i"}
    if size:
        query["sizes"] = {"$elemMatch": {"size": size}}
    
    total_count = products_collection.count_documents(query)
    cursor = products_collection.find(query).sort("_id").skip(offset).limit(limit)
    products = [ProductListItem(**{**doc, "id": str(doc["_id"])}) for doc in cursor]
    
    page = Pagination(
        next=offset + limit if offset + limit < total_count else None,
        limit=limit,
        previous=offset - limit if offset - limit >= 0 else None
    )
    return ProductListResponse(data=products, page=page)

@app.post("/orders", response_model=OrderResponse, status_code=201)
async def create_order(order: OrderCreate):
    # Transform and validate items
    transformed_items = []
    for item in order.items:
        # Access productId from productDetails
        product_id = item.productDetails.productId
        product = products_collection.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(status_code=400, detail=f"Product {product_id} not found")
        # Store flat structure after validation
        transformed_items.append({"productId": product_id, "qty": item.qty})
    
    order_dict = {"userId": order.userId, "items": transformed_items}
    result = orders_collection.insert_one(order_dict)
    return {"id": str(result.inserted_id)}

@app.get("/orders/{user_id}", response_model=OrderListResponse)
async def list_orders(user_id: str, limit: int = 10, offset: int = 0):
    # Debug: Check if orders exist for the user
    order_count = orders_collection.count_documents({"userId": {"$regex": f"^{user_id}$", "$options": "i"}})
    print(f"Orders count for {user_id}: {order_count}")

    # Fetch orders with pagination without lookup
    query = {"userId": {"$regex": f"^{user_id}$", "$options": "i"}}
    total_count = orders_collection.count_documents(query)
    cursor = orders_collection.find(query).sort("_id").skip(offset).limit(limit)
    orders = []
    
    for doc in cursor:
        enriched_items = []
        order_total = 0
        for item in doc.get("items", []):
            product = products_collection.find_one({"_id": ObjectId(item["productId"])})
            if product:
                product_details = ProductDetails(productId=item["productId"], name=product["name"])
                enriched_item = OrderItem(productDetails=product_details, qty=item["qty"])
                enriched_items.append(enriched_item)
                order_total += item["qty"] * product.get("price", 0)
        orders.append(OrderListItem(id=str(doc["_id"]), userId=doc["userId"], items=enriched_items, total=order_total))

    page = Pagination(
        next=offset + limit if offset + limit < total_count else None,
        limit=limit,
        previous=offset - limit if offset - limit >= 0 else None
    )
    # Calculate root-level total as sum of per-order totals
    root_total = sum(o.total for o in orders if o.total is not None) if orders else 0
    return OrderListResponse(data=orders, page=page, total=root_total)