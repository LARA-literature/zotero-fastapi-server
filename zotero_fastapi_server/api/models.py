from pydantic import BaseModel, Field
from typing import List, Optional, Dict


class Creator(BaseModel):
    creatorType: str
    primary: Optional[bool] = False
    firstName: Optional[str] = None
    lastName: Optional[str] = None

class Tag(BaseModel):
    tag: str

class Note(BaseModel):
    note: str

class LibraryInfo(BaseModel):
    type: str
    id: int
    name: str
    links: Dict[str, Dict[str, str]]

class Links(BaseModel):
    self: Dict[str, str]
    alternate: Dict[str, str]

class Meta(BaseModel):
    numChildren: int
    creatorSummary: Optional[str] = None
    parsedDate: Optional[str] = None

class Data(BaseModel):
    key: str
    version: int
    itemType: str
    title: str
    creators: List[Creator] = []
    abstractNote: str
    websiteTitle: str
    websiteType: str
    date: str
    shortTitle: str
    url: str
    accessDate: str
    language: str
    rights: str
    extra: str
    tags: List[Dict[str, str]]
    collections: List[str]
    relations: Dict[str, str]
    dateAdded: str
    dateModified: str

class Item(BaseModel):
    itemType: str
    title: str
    abstractNote: Optional[str] = None
    creators: List[Creator] = []
    tags: List[Tag] = []
    notes: List[Note] = []
    dateAdded: str
    dateModified: str

    class Config:
        from_attributes = True

class ItemResponse(BaseModel):
    key: str
    version: int
    library: LibraryInfo
    links: Links
    meta: Meta
    data: Data

    class Config:
        from_attributes = True

class ItemCreate(BaseModel):
    key: str
    version: int
    library: LibraryInfo
    links: Links
    meta: Meta
    data: Data



class CollectionData(BaseModel):
    key: str
    version: int
    name: str
    parentCollection: bool = False
    relations: Dict = {}

class CollectionMeta(BaseModel):
    numCollections: int
    numItems: int = 0

class CollectionResponse(BaseModel):
    key: str
    version: int
    library: LibraryInfo
    links: Links
    meta: CollectionMeta
    data: CollectionData

    class Config:
        from_attributes = True

class CreateCollection(BaseModel):
    key: str
    version: int
    library: LibraryInfo
    links: Links
    meta: CollectionMeta
    data: CollectionData