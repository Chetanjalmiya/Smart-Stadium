"""API routes for the Food & Beverage module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.food_service import FoodService
from app.schemas.food import (
    MenuItemCreate,
    MenuItemResponse,
    FoodOrderCreate,
    FoodOrderResponse,
    FoodOrderStatusUpdate,
)
from app.models.food import OrderStatus
from app.utils.responses import success_response

router = APIRouter(prefix="/food", tags=["Food & Beverage"])


@router.post("/menu", response_model=dict, status_code=201, summary="Add a menu item")
def create_menu_item(payload: MenuItemCreate, db: Session = Depends(get_db)) -> dict:
    item = FoodService(db).create_menu_item(payload)
    return success_response(MenuItemResponse.model_validate(item).model_dump(), "Menu item added.")


@router.get("/menu", response_model=dict, summary="List menu items")
def list_menu(
    category: Optional[str] = Query(default=None),
    available_only: bool = Query(default=False),
    db: Session = Depends(get_db),
) -> dict:
    items = FoodService(db).list_menu_items(category, available_only)
    data = [MenuItemResponse.model_validate(i).model_dump() for i in items]
    return success_response(data, f"Retrieved {len(data)} menu item(s).")


@router.post("/orders", response_model=dict, status_code=201, summary="Place a food order")
def place_order(payload: FoodOrderCreate, db: Session = Depends(get_db)) -> dict:
    order = FoodService(db).place_order(payload)
    return success_response(FoodOrderResponse.model_validate(order).model_dump(), "Order placed successfully.")


@router.get("/orders", response_model=dict, summary="List food orders")
def list_orders(status: Optional[OrderStatus] = Query(default=None), db: Session = Depends(get_db)) -> dict:
    orders = FoodService(db).list_orders(status)
    data = [FoodOrderResponse.model_validate(o).model_dump() for o in orders]
    return success_response(data, f"Retrieved {len(data)} order(s).")


@router.get("/orders/{order_id}", response_model=dict, summary="Get order by ID")
def get_order(order_id: int, db: Session = Depends(get_db)) -> dict:
    order = FoodService(db).get_order(order_id)
    return success_response(FoodOrderResponse.model_validate(order).model_dump())


@router.patch("/orders/{order_id}/status", response_model=dict, summary="Update order status")
def update_order_status(order_id: int, payload: FoodOrderStatusUpdate, db: Session = Depends(get_db)) -> dict:
    order = FoodService(db).update_order_status(order_id, payload)
    return success_response(FoodOrderResponse.model_validate(order).model_dump(), "Order status updated.")
