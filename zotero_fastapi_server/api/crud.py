
from typing import List
from .database import item_collection
from .models import Item

async def get_all_items() -> List[Item]:
    items = []
    async for item in item_collection.find():
        items.append(Item(**item))
    return items

async def get_item(item_id: str) -> Item:
    item = await item_collection.find_one({"_id": item_id})
    if item:
        return Item(**item)

async def create_item(item: Item) -> Item:
    item_dict = item.dict()
    await item_collection.insert_one(item_dict)
    return item

async def update_item(item_id: str, item: Item) -> Item:
    await item_collection.update_one({"_id": item_id}, {"$set": item.dict()})
    return await get_item(item_id)

async def delete_item(item_id: str):
    await item_collection.delete_one({"_id": item_id})
