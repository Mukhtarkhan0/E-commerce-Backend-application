# from pydantic import BaseModel, validator
# from typing import List, Optional
# from datetime import datetime

# class SizeItem(BaseModel):
#     size: str
#     quantity: int

#     @validator("quantity")
#     def quantity_must_be_positive(cls, v):
#         if v <= 0:
#             raise ValueError("quantity must be positive")
#         return v

# class ProductCreate(BaseModel):
#     name: str
#     price: float
#     sizes: List[SizeItem]

#     @validator("price")
#     def price_must_be_positive(cls, v):
#         if v <= 0:
#             raise ValueError("price must be positive")
#         return v

# class ProductResponse(BaseModel):
#     id: str
#     name: str
#     price: float

# class OrderItem(BaseModel):
#     productId: str
#     qty: int

#     @validator("qty")
#     def qty_must_be_positive(cls, v):
#         if v <= 0:
#             raise ValueError("qty must be positive")
#         return v

# class OrderCreate(BaseModel):
#     userId: str
#     items: List[OrderItem]

# class OrderResponse(BaseModel):
#     id: str

# class Pagination(BaseModel):
#     next: Optional[int] = None
#     limit: Optional[int] = None
#     previous: Optional[int] = None

# class ProductListResponse(BaseModel):
#     data: List[ProductResponse]
#     page: Pagination

# class OrderListResponse(BaseModel):
#     data: List[OrderResponse]
#     page: Pagination
#     total: Optional[float] = None