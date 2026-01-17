from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class NoteBase(BaseModel):
    title: str
    content: Optional[str] = ""
    is_folder: bool = False
    parent_id: Optional[int] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    parent_id: Optional[int] = None

class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    children: List['NoteResponse'] = []

    class Config:
        from_attributes = True

# Update forward references for recursive model
NoteResponse.model_rebuild()
