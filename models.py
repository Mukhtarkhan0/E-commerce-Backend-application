from pydantic import BaseModel, field_validator
from typing import List, Optional
from datetime import datetime

class SizeItem(BaseModel):
    size: str
    quantity: int

    @field_validator("quantity")
    @classmethod
    def quantity_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("quantity must be positive")
        return v

class ProductCreate(BaseModel):
    name: str
    price: float
    sizes: List[SizeItem]

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("price must be positive")
        return v

class ProductResponse(BaseModel):
    id: str

class ProductListItem(BaseModel):
    id: str
    name: str
    price: float
    sizes: List[SizeItem]

class ProductDetails(BaseModel):
    productId: str
    name: str

class OrderItem(BaseModel):
    productDetails: ProductDetails
    qty: int

    @field_validator("qty")
    @classmethod
    def qty_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("qty must be positive")
        return v

class OrderCreate(BaseModel):
    userId: str
    items: List[OrderItem]

class OrderResponse(BaseModel):
    id: str

class OrderListItem(BaseModel):
    id: str
    userId: str
    items: List[OrderItem]
    total: Optional[float] = None

class Pagination(BaseModel):
    next: Optional[int] = None
    limit: Optional[int] = None
    previous: Optional[int] = None

class ProductListResponse(BaseModel):
    data: List[ProductListItem]
    page: Pagination

class OrderListResponse(BaseModel):
    data: List[OrderListItem]
    page: Pagination
    total: Optional[float] = None