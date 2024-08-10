from pydantic import BaseModel, Field
from typing import List, Optional

class Creator(BaseModel):
    creatorType: str
    primary: Optional[bool] = False

class Tag(BaseModel):
    tag: str

class Note(BaseModel):
    note: str

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
        orm_mode = True
