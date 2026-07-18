"""Pydantic schemas for the Food & Beverage module."""
from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict
from app.models.food import OrderStatus


class MenuItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: str = Field(..., min_length=1, max_length=50)
    price: float = Field(..., gt=0)
    stall_location: str = Field(default="Stall 1", max_length=100)
    description: Optional[str] = Field(default=None, max_length=255)
    is_available: bool = True


class MenuItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    category: str
    price: float
    is_available: bool
    stall_location: str
    description: Optional[str] = None
    created_at: datetime


class FoodOrderItemCreate(BaseModel):
    menu_item_id: int = Field(..., gt=0)
    quantity: int = Field(..., gt=0, le=50)


class FoodOrderCreate(BaseModel):
    customer_name: str = Field(..., min_length=1, max_length=100)
    seat_number: Optional[str] = Field(default=None, max_length=20)
    items: List[FoodOrderItemCreate] = Field(..., min_length=1)


class FoodOrderItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    menu_item_id: int
    quantity: int
    unit_price: float


class FoodOrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_name: str
    seat_number: Optional[str] = None
    status: OrderStatus
    total_amount: float
    created_at: datetime
    updated_at: datetime
    items: List[FoodOrderItemResponse] = []


class FoodOrderStatusUpdate(BaseModel):
    status: OrderStatus
