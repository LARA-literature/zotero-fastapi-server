
from fastapi import APIRouter, Response, HTTPException, Query, status


from typing import List, Optional
from ..database import database as db
from ..models import CollectionData, CollectionResponse, CreateCollection, Item, ItemCreate, ItemResponse
from ..schemata import ItemSchema
from ..crud import ( get_all_collections,
     get_items_in_collection,
    get_top_items_in_collection, create_collection
)

router = APIRouter()

@router.get("/collections", response_model=List[CollectionResponse])
async def list_all_collections(
    direction: Optional[str] = Query("asc", regex="^(asc|desc)$"),
    format: Optional[str] = Query("json", regex="^(json|xml)$"),
    limit: Optional[int] = Query(100, ge=1, le=1000),
    sort: Optional[str] = Query("dateModified", regex="^(dateModified|name|dateAdded)$")):
    """
    Retrieve all collections in the library.
    """
    collections = await get_all_collections(db, direction, format, limit, sort)
    if not collections:
        raise HTTPException(status_code=404, detail="No collections found")
    return collections

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


@router.post("/collections", response_model=CollectionResponse)
async def add_collection(collection: CreateCollection):
    """
    Create a new collection in the library.
    """
    new_collection = await create_collection(db, collection)
    
    # Construct the response in the expected format
    collection_response = {
        "key": str(new_collection["_id"]),
        "version": new_collection["version"],
        "library": {
            "type": "user",
            "id": 475425,  # Fixed user ID for demonstration
            "name": "Z public library",  # Example name
            "links": {
                "alternate": {
                    "href": "https://www.zotero.org/z_public_library",
                    "type": "text/html"
                }
            }
        },
        "links": {
            "self": {
                "href": f"https://api.zotero.org/users/475425/collections/{new_collection['key']}",
                "type": "application/json"
            },
            "alternate": {
                "href": f"https://www.zotero.org/z_public_library/collections/{new_collection['key']}",
                "type": "text/html"
            }
        },
        "meta": {
            "numCollections": new_collection["meta"]["numCollections"],
            "numItems": new_collection["meta"]["numItems"]
        },
        "data": {
            "key": str(new_collection["data"]["key"]),
            "version": new_collection["data"]["version"],
            "name": new_collection["data"]["name"],
            "parentCollection": new_collection["data"]["parentCollection"],
            "relations": new_collection["data"]["relations"]
        }
    }
    
    return CollectionResponse(**collection_response)