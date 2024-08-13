import logging
import uuid
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from .models import CollectionData, CollectionResponse, CreateCollection, Item, ItemCreate, ItemResponse

logger = logging.getLogger(__name__)


# Function to get all items (excluding trash)
async def get_all_items(db: AsyncIOMotorDatabase):
    items = []
    async for item in db.items.find({"trashed": {"$ne": True}}):  # Assuming a "trashed" flag
        items.append(ItemResponse(**item))
    return items


# # Function to get top-level items
# async def get_top_level_items(db: AsyncIOMotorDatabase):
#     items = []
#     async for item in db.items.find({"parentItem": {"$exists": False}, "trashed": {"$ne": True}}):
#         items.append(ItemResponse(**item))
#     return items

# CRUD operations for top level items


async def get_top_level_items(db: AsyncIOMotorDatabase):
    items = []
    async for item in db.items.find({"parentItem": {"$exists": False}}):
        item_response = {
            "key": str(item["_id"]),
            "version": item.get("version", 1),
            "library": {
                "type": "user",
                "id": 475425,  # Assuming a fixed user ID for demonstration
                "name": "Z public library",  # Example name, this should be dynamic based on actual data
                "links": {"alternate": {"href": f"https://www.zotero.org/z_public_library", "type": "text/html"}},
            },
            "links": {
                "self": {
                    "href": f"https://api.zotero.org/users/475425/items/{item['_id']}",
                    "type": "application/json",
                },
                "alternate": {
                    "href": f"https://www.zotero.org/z_public_library/items/{item['_id']}",
                    "type": "text/html",
                },
            },
            "meta": {
                "numChildren": item.get("numChildren", 0),
                "creatorSummary": item.get("creatorSummary", ""),
                "parsedDate": item.get("parsedDate", ""),
            },
            "data": {
                "key": str(item["_id"]),
                "version": item.get("version", 1),
                "itemType": item.get("itemType", ""),
                "title": item.get("title", ""),
                "creators": item.get("creators", []),
                "abstractNote": item.get("abstractNote", ""),
                "websiteTitle": item.get("websiteTitle", ""),
                "websiteType": item.get("websiteType", ""),
                "date": item.get("date", ""),
                "shortTitle": item.get("shortTitle", ""),
                "url": item.get("url", ""),
                "accessDate": item.get("accessDate", ""),
                "language": item.get("language", ""),
                "rights": item.get("rights", ""),
                "extra": item.get("extra", ""),
                "tags": item.get("tags", []),
                "collections": item.get("collections", []),
                "relations": item.get("relations", {}),
                "dateAdded": item.get("dateAdded", ""),
                "dateModified": item.get("dateModified", ""),
            },
        }
        items.append(ItemResponse(**item_response))
    return items


async def get_all_collections(
    db: AsyncIOMotorDatabase,
    user_id: str,
    direction: str = "asc",
    format: str = "json",
    limit: int = 100,
    sort: str = "dateModified",
) -> list[CollectionResponse]:
    """
    Fetch collections from the database with sorting and limiting.
    """
    sort_direction = 1 if direction == "asc" else -1
    sort_field = sort
    collections = []
    async for collection in db.collections.find():
        collection_response = {
            "key": str(collection["_id"]),
            "version": collection.get("version", 1),
            "library": {
                "type": "user",
                "id": 475425,  # Fixed user ID for demonstration
                "name": "Z public library",  # Example name
                "links": {"alternate": {"href": "https://www.zotero.org/z_public_library", "type": "text/html"}},
            },
            "links": {
                "self": {
                    "href": f"https://api.zotero.org/users/475425/collections/{collection['_id']}",
                    "type": "application/json",
                },
                "alternate": {
                    "href": f"https://www.zotero.org/z_public_library/collections/{collection['_id']}",
                    "type": "text/html",
                },
            },
            "meta": {"numCollections": collection.get("numCollections", 0), "numItems": collection.get("numItems", 0)},
            "data": {
                "key": str(collection["_id"]),
                "version": collection.get("version", 1),
                "name": collection.get("name", ""),
                "parentCollection": collection.get("parentCollection", False),
                "relations": collection.get("relations", {}),
            },
        }
        collections.append(CollectionResponse(**collection_response))
    return collections


async def create_collection(db: AsyncIOMotorDatabase, collection: CreateCollection):
    curr_key = str(uuid.uuid4())[:8]
    new_collection = {
        "key": collection.key,
        "version": collection.version,
        "library": {
            "type": "user",
            "id": 475425,  # Fixed user ID for demonstration
            "name": "Z public library",  # Example name
            "links": {"alternate": {"href": "https://www.zotero.org/z_public_library", "type": "text/html"}},
        },
        "links": {
            "self": {
                "href": f"https://api.zotero.org/users/475425/collections/{collection.key}",
                "type": "application/json",
            },
            "alternate": {
                "href": f"https://www.zotero.org/z_public_library/collections/{collection.key}",
                "type": "text/html",
            },
        },
        "meta": {"numCollections": collection.meta.numCollections, "numItems": collection.meta.numItems},
        "data": {
            "key": collection.data.key,
            "version": collection.data.version,
            "name": collection.data.name,
            "parentCollection": collection.data.parentCollection,
            "relations": collection.data.relations,
        },
    }

    # {
    #     "name": collection.name,
    #     "parentCollection": collection.parentCollection,
    #     "relations": collection.relations,
    #     "numCollections": 0,
    #     "numItems": 0,
    #     "version": 1  # Initial version
    # }
    result = await db.collections.insert_one(new_collection)
    new_collection["_id"] = str(result.inserted_id)
    return new_collection


# Function to get items in the trash
async def get_trashed_items(db: AsyncIOMotorDatabase):
    items = []
    async for item in db.items.find({"trashed": True}):  # Assuming a "trashed" flag
        items.append(ItemResponse(**item))
    return items


# Function to get a specific item by its ID
async def get_item(db: AsyncIOMotorDatabase, item_id: str):
    item = await db.items.find_one({"_id": ObjectId(item_id)})
    if item:
        return ItemResponse(**item)
    return None


# Function to get children of a specific item
async def get_child_items(db: AsyncIOMotorDatabase, item_id: str):
    items = []
    async for item in db.items.find({"parentItem": item_id}):
        items.append(ItemResponse(**item))
    return items


# Function to get items in "My Publications"
async def get_publication_items(db: AsyncIOMotorDatabase):
    items = []
    async for item in db.items.find({"isPublication": True}):  # Assuming an "isPublication" flag
        items.append(ItemResponse(**item))
    return items


# Function to get items in a specific collection
async def get_items_in_collection(db: AsyncIOMotorDatabase, collection_id: str):
    items = []
    async for item in db.items.find({"collections": collection_id}):
        items.append(ItemResponse(**item))
    return items


# Function to get top-level items in a specific collection
async def get_top_items_in_collection(db: AsyncIOMotorDatabase, collection_id: str):
    items = []
    async for item in db.items.find({"collections": collection_id, "parentItem": {"$exists": False}}):
        items.append(ItemResponse(**item))
    return items


# Function to create an item
# async def create_item(db: AsyncIOMotorDatabase, item: Item) -> Item:
#     item_dict = item.model_dump()
#     try:
#         await db.items.insert_one(item_dict)
#     except Exception as e:
#         logger.error(f'Error inserting item into MongoDB: {e}')

#     return item


async def create_item(db: AsyncIOMotorDatabase, item: ItemCreate):
    item_dict = item.dict(by_alias=True)
    result = await db.items.insert_one(item_dict)
    return str(result.inserted_id)


# from typing import List
# from .database import item_collection
# from .models import Item, ItemResponse
# from motor.motor_asyncio import AsyncIOMotorDatabase

# async def get_all_items() -> List[Item]:
#     items = []
#     async for item in item_collection.find():
#         items.append(Item(**item))
#     return items

# async def get_item(item_id: str) -> Item:
#     item = await item_collection.find_one({"_id": item_id})
#     if item:
#         return Item(**item)

# async def create_item(item: Item) -> Item:
#     item_dict = item.model_dump()
#     try:
#         await item_collection.insert_one(item_dict)
#     except Exception as e:
#         logger.error(f'Error inserting items into MongoDB: {e}')

#     return item

# async def update_item(item_id: str, item: Item) -> Item:
#     try:
#         await item_collection.update_one({"_id": item_id}, {"$set": item.model_dump()})
#     except Exception as e:
#         logger.error(f'Error updating items in MongoDB: {e}')
#     return await get_item(item_id)

# async def delete_item(item_id: str):
#     try:
#         await item_collection.delete_one({"_id": item_id})
#     except Exception as e:
#         logger.error(f'Error deleting items from MongoDB: {e}')
