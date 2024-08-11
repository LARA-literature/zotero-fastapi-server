from fastapi import APIRouter, HTTPException
from typing import List
from ..crud import get_all_items, get_item, create_item, update_item, delete_item
from ..schemata import ItemSchema
from ..models import Item

router = APIRouter()

@router.get("/", response_model=List[ItemSchema])
async def read_items():
    return await get_all_items()

@router.get("/{item_id}", response_model=ItemSchema)
async def read_item(item_id: str):
    item = await get_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/", response_model=ItemSchema)
async def create_item_endpoint(item: ItemSchema):
    new_item = Item(**item.model_dump())
    created_item = await create_item(new_item)
    return created_item

@router.put("/{item_id}", response_model=ItemSchema)
async def update_item_endpoint(item_id: str, item: ItemSchema):
    updated_item = Item(**item.model_dump())
    updated = await update_item(item_id, updated_item)
    if updated is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated

@router.delete("/{item_id}")
async def delete_item_endpoint(item_id: str):
    await delete_item(item_id)
    return {"message": "Item deleted successfully"}
