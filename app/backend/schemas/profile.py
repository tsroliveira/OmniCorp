from pydantic import BaseModel
from typing import List, Optional
from app.backend.schemas.permission import PermissionResponse

class ProfileBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(ProfileBase):
    name: Optional[str] = None

class ProfileResponse(ProfileBase):
    id: int
    permissions: List[PermissionResponse] = []

    class Config:
        orm_mode = True 