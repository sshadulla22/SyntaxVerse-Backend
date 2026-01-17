from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class NoteBase(BaseModel):
    title: str
    content: Optional[str] = ""
    is_folder: bool = False
    parent_id: Optional[int] = None
    cover_image: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    parent_id: Optional[int] = None
    cover_image: Optional[str] = None

class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    children: List['NoteResponse'] = []

    class Config:
        from_attributes = True

# Update forward references for recursive model
# Update forward references for recursive model
NoteResponse.model_rebuild()

class ExecuteRequest(BaseModel):
    language: str
    version: str = "*"
    files: List[dict]
    stdin: str = ""
    args: List[str] = []
    compile_timeout: int = 10000
    run_timeout: int = 3000
    compile_memory_limit: int = -1
    run_memory_limit: int = -1
