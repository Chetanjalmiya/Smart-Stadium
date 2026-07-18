"""Food & Beverage module models."""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Float, Enum, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database.base import Base


class OrderStatus(str, enum.Enum):
    PLACED = "placed"
    PREPARING = "preparing"
    READY = "ready"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class MenuItem(Base):
    """Represents an item available for order in the stadium."""

    __tablename__ = "menu_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    price = Column(Float, nullable=False)
    is_available = Column(Boolean, default=True)
    stall_location = Column(String(100), nullable=False, default="Stall 1")
    description = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class FoodOrder(Base):
    """Represents a customer order comprised of multiple menu items."""

    __tablename__ = "food_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(100), nullable=False)
    seat_number = Column(String(20), nullable=True)
    status = Column(Enum(OrderStatus), nullable=False, default=OrderStatus.PLACED)
    total_amount = Column(Float, nullable=False, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    items = relationship("FoodOrderItem", back_populates="order", cascade="all, delete-orphan")


class FoodOrderItem(Base):
    """Represents a single line item within a food order."""

    __tablename__ = "food_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("food_orders.id"), nullable=False)
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Float, nullable=False)

    order = relationship("FoodOrder", back_populates="items")
    menu_item = relationship("MenuItem")
