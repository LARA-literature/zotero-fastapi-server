def individual_serializer(book) -> dict:
    return {
        "id": str(book["_id"]),
        "title": book["title"],
        "description": book["description"],
        "borrowed": book["borrowed"]
    }
 
def books_serializer(books) -> list:
    return [individual_serializer(book) for book in books]


from pydantic import BaseModel
from typing import List, Optional

class CreatorSchema(BaseModel):
    creatorType: str
    primary: Optional[bool]

class TagSchema(BaseModel):
    tag: str

class NoteSchema(BaseModel):
    note: str

class ItemSchema(BaseModel):
    itemType: str
    title: str
    abstractNote: Optional[str]
    creators: List[CreatorSchema]
    tags: List[TagSchema]
    notes: List[NoteSchema]
    dateAdded: str
    dateModified: str

    class Config:
        orm_mode = True
