
from typing import List
import logging
from .database import item_collection
from .models import Item


logger = logging.getLogger(__name__)

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
    item_dict = item.model_dump()
    try:
        await item_collection.insert_one(item_dict)
    except Exception as e:
        logger.error(f'Error inserting items into MongoDB: {e}')

    return item

async def update_item(item_id: str, item: Item) -> Item:
    try:
        await item_collection.update_one({"_id": item_id}, {"$set": item.model_dump()})
    except Exception as e:
        logger.error(f'Error updating items in MongoDB: {e}')
    return await get_item(item_id)

async def delete_item(item_id: str):
    try:
        await item_collection.delete_one({"_id": item_id})
    except Exception as e:
        logger.error(f'Error deleting items from MongoDB: {e}')
