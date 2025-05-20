from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.backend.database.session import get_db
from app.backend.models.role import Role, Permission
from app.backend.schemas.role import RoleCreate, RoleUpdate, RoleOut, PermissionCreate, PermissionOut
from app.backend.services.role_service import (
    create_role,
    get_role,
    get_roles,
    update_role,
    delete_role,
    create_permission,
    get_permissions
)

router = APIRouter(
    prefix="/api/roles",
    tags=["roles"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=RoleOut, status_code=status.HTTP_201_CREATED)
def create_new_role(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db=db, role=role)

@router.get("/", response_model=List[RoleOut])
def read_roles(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    roles = get_roles(db, skip=skip, limit=limit)
    return roles

@router.get("/{role_id}", response_model=RoleOut)
def read_role(role_id: int, db: Session = Depends(get_db)):
    db_role = get_role(db, role_id=role_id)
    if db_role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return db_role

@router.put("/{role_id}", response_model=RoleOut)
def update_existing_role(role_id: int, role: RoleUpdate, db: Session = Depends(get_db)):
    return update_role(db=db, role_id=role_id, role=role)

@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_role(role_id: int, db: Session = Depends(get_db)):
    delete_role(db=db, role_id=role_id)
    return

@router.post("/permissions/", response_model=PermissionOut, status_code=status.HTTP_201_CREATED)
def create_new_permission(permission: PermissionCreate, db: Session = Depends(get_db)):
    return create_permission(db=db, permission=permission)

@router.get("/permissions/", response_model=List[PermissionOut])
def read_permissions(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_permissions(db, skip=skip, limit=limit) 