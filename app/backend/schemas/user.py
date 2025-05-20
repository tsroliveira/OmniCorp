from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class Role(RoleBase):
    id: int

    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    name: str
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    pass


class Permission(PermissionBase):
    id: int

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    is_active: bool = True
    is_ad_user: bool = True


class UserCreate(UserBase):
    password: Optional[str] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role_id: Optional[int] = None


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    role: Optional[Role] = None

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str
    permissions: List[str] = []


class ModuleBase(BaseModel):
    name: str
    description: Optional[str] = None
    url: str
    icon: Optional[str] = None
    is_active: bool = True
    required_permission_id: int


class ModuleCreate(ModuleBase):
    pass


class Module(ModuleBase):
    id: int

    class Config:
        from_attributes = True 