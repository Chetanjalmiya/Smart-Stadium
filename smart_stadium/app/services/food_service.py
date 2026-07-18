"""Business logic for the Food & Beverage module."""
from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.food import MenuItem, FoodOrder, FoodOrderItem, OrderStatus
from app.schemas.food import MenuItemCreate, FoodOrderCreate, FoodOrderStatusUpdate
from app.utils.exceptions import NotFoundException, ValidationException


class FoodService:
    """Encapsulates menu management and order placement logic."""

    def __init__(self, db: Session):
        self.db = db

    def create_menu_item(self, payload: MenuItemCreate) -> MenuItem:
        item = MenuItem(**payload.model_dump())
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def list_menu_items(
        self, category: Optional[str] = None, available_only: bool = False
    ) -> List[MenuItem]:
        query = self.db.query(MenuItem)
        if category:
            query = query.filter(MenuItem.category == category)
        if available_only:
            query = query.filter(MenuItem.is_available.is_(True))
        return query.order_by(MenuItem.category.asc(), MenuItem.name.asc()).all()

    def get_menu_item(self, item_id: int) -> MenuItem:
        item = self.db.query(MenuItem).filter(MenuItem.id == item_id).first()
        if not item:
            raise NotFoundException("Menu item", item_id)
        return item

    def place_order(self, payload: FoodOrderCreate) -> FoodOrder:
        order = FoodOrder(customer_name=payload.customer_name, seat_number=payload.seat_number)
        total = 0.0
        order_items = []

        for line in payload.items:
            menu_item = self.get_menu_item(line.menu_item_id)
            if not menu_item.is_available:
                raise ValidationException(f"'{menu_item.name}' is currently unavailable.")
            subtotal = menu_item.price * line.quantity
            total += subtotal
            order_items.append(
                FoodOrderItem(
                    menu_item_id=menu_item.id,
                    quantity=line.quantity,
                    unit_price=menu_item.price,
                )
            )

        order.total_amount = round(total, 2)
        order.items = order_items
        self.db.add(order)
        self.db.commit()
        self.db.refresh(order)
        return order

    def get_order(self, order_id: int) -> FoodOrder:
        order = self.db.query(FoodOrder).filter(FoodOrder.id == order_id).first()
        if not order:
            raise NotFoundException("Food order", order_id)
        return order

    def list_orders(self, status: Optional[OrderStatus] = None) -> List[FoodOrder]:
        query = self.db.query(FoodOrder)
        if status:
            query = query.filter(FoodOrder.status == status)
        return query.order_by(FoodOrder.created_at.desc()).all()

    def update_order_status(self, order_id: int, payload: FoodOrderStatusUpdate) -> FoodOrder:
        order = self.get_order(order_id)
        order.status = payload.status
        self.db.commit()
        self.db.refresh(order)
        return order
