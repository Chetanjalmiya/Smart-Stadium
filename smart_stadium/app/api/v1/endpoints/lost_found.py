"""API routes for the Lost & Found module."""
from typing import Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.services.lost_found_service import LostFoundService
from app.schemas.lost_found import LostFoundItemCreate, LostFoundItemResponse, LostFoundStatusUpdate
from app.models.lost_found import LostFoundStatus, LostFoundType
from app.utils.responses import success_response

router = APIRouter(prefix="/lost-found", tags=["Lost & Found"])


@router.post("", response_model=dict, status_code=201, summary="Report a lost or found item")
def create_item(payload: LostFoundItemCreate, db: Session = Depends(get_db)) -> dict:
    item = LostFoundService(db).create_item(payload)
    return success_response(LostFoundItemResponse.model_validate(item).model_dump(), "Item reported successfully.")


@router.get("", response_model=dict, summary="List lost & found items")
def list_items(
    item_type: Optional[LostFoundType] = Query(default=None),
    status: Optional[LostFoundStatus] = Query(default=None),
    db: Session = Depends(get_db),
) -> dict:
    items = LostFoundService(db).list_items(item_type, status)
    data = [LostFoundItemResponse.model_validate(i).model_dump() for i in items]
    return success_response(data, f"Retrieved {len(data)} item(s).")


@router.get("/search", response_model=dict, summary="Search lost & found items by keyword")
def search_items(keyword: str = Query(..., min_length=1), db: Session = Depends(get_db)) -> dict:
    items = LostFoundService(db).search_items(keyword)
    data = [LostFoundItemResponse.model_validate(i).model_dump() for i in items]
    return success_response(data, f"Found {len(data)} matching item(s).")


@router.get("/{item_id}", response_model=dict, summary="Get lost & found item by ID")
def get_item(item_id: int, db: Session = Depends(get_db)) -> dict:
    item = LostFoundService(db).get_item(item_id)
    return success_response(LostFoundItemResponse.model_validate(item).model_dump())


@router.patch("/{item_id}/status", response_model=dict, summary="Update item status")
def update_status(item_id: int, payload: LostFoundStatusUpdate, db: Session = Depends(get_db)) -> dict:
    item = LostFoundService(db).update_status(item_id, payload)
    return success_response(LostFoundItemResponse.model_validate(item).model_dump(), "Status updated successfully.")
