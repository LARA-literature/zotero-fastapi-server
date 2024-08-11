from fastapi import APIRouter, HTTPException
from typing import List
from ..database import database as db
from ..models import Item, ItemResponse
from ..schemata import ItemSchema
from ..crud import (
    get_all_items, get_top_level_items, get_trashed_items, get_item, create_item,
    get_child_items, get_publication_items, get_items_in_collection,
    get_top_items_in_collection
)

router = APIRouter()

# Route to get all items (excluding trash)
@router.get("/items", response_model=List[ItemResponse])
async def list_all_items():
    items = await get_all_items(db)
    if not items:
        raise HTTPException(status_code=404, detail="No items found")
    return items

@router.post("/items", response_model=ItemSchema)
async def create_item_endpoint(item: ItemSchema):
     new_item = Item(**item.model_dump())
     created_item = await create_item(db, new_item)
     return created_item

# Route to get all top-level items
@router.get("/items/top", response_model=List[ItemResponse])
async def list_top_level_items():
    items = await get_top_level_items(db)
    if not items:
        raise HTTPException(status_code=404, detail="No top-level items found")
    return items

# Route to get items in the trash
@router.get("/items/trash", response_model=List[ItemResponse])
async def list_trashed_items():
    items = await get_trashed_items(db)
    if not items:
        raise HTTPException(status_code=404, detail="No trashed items found")
    return items

# Route to get a specific item by its ID
@router.get("/items/{item_id}", response_model=ItemResponse)
async def retrieve_item(item_id: str):
    item = await get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Route to get children of a specific item
@router.get("/items/{item_id}/children", response_model=List[ItemResponse])
async def list_child_items(item_id: str):
    items = await get_child_items(db, item_id)
    if not items:
        raise HTTPException(status_code=404, detail="No child items found")
    return items

# Route to get items in "My Publications"
@router.get("/publications/items", response_model=List[ItemResponse])
async def list_publication_items():
    items = await get_publication_items(db)
    if not items:
        raise HTTPException(status_code=404, detail="No publication items found")
    return items

# Route to get items in a specific collection
@router.get("/collections/{collection_id}/items", response_model=List[ItemResponse])
async def list_items_in_collection(collection_id: str):
    items = await get_items_in_collection(db, collection_id)
    if not items:
        raise HTTPException(status_code=404, detail="No items found in this collection")
    return items

# Route to get top-level items in a specific collection
@router.get("/collections/{collection_id}/items/top", response_model=List[ItemResponse])
async def list_top_items_in_collection(collection_id: str):
    items = await get_top_items_in_collection(db, collection_id)
    if not items:
        raise HTTPException(status_code=404, detail="No top-level items found in this collection")
    return items


## old code

# from fastapi import APIRouter, HTTPException
# from typing import List
# from ..crud import get_all_items, get_item, create_item, update_item, delete_item
# from ..schemata import ItemSchema
# from ..models import Item

# router = APIRouter()

# @router.get("/", response_model=List[ItemSchema])
# async def read_items():
#     return await get_all_items()

# @router.get("/{item_id}", response_model=ItemSchema)
# async def read_item(item_id: str):
#     item = await get_item(item_id)
#     if item is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return item

# @router.post("/", response_model=ItemSchema)
# async def create_item_endpoint(item: ItemSchema):
#     new_item = Item(**item.model_dump())
#     created_item = await create_item(new_item)
#     return created_item

# @router.put("/{item_id}", response_model=ItemSchema)
# async def update_item_endpoint(item_id: str, item: ItemSchema):
#     updated_item = Item(**item.model_dump())
#     updated = await update_item(item_id, updated_item)
#     if updated is None:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return updated

# @router.delete("/{item_id}")
# async def delete_item_endpoint(item_id: str):
#     await delete_item(item_id)
#     return {"message": "Item deleted successfully"}

