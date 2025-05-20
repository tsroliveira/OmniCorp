from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.backend.database.session import get_db
from app.backend.models.permission import Permission
from app.backend.schemas.permission import PermissionCreate, PermissionResponse
from app.backend.middleware.auth_middleware import check_permission
from app.backend.services.redis_service import redis_service

router = APIRouter()

@router.post("/permissions", response_model=PermissionResponse)
def create_permission(
    permission: PermissionCreate,
    db: Session = Depends(get_db),
    _ = Depends(check_permission("permission:create"))
):
    db_permission = Permission(
        name=permission.name,
        description=permission.description
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    return db_permission

@router.get("/permissions", response_model=List[PermissionResponse])
def list_permissions(
    db: Session = Depends(get_db),
    _ = Depends(check_permission("permission:read"))
):
    return db.query(Permission).all()

@router.get("/permissions/{permission_id}", response_model=PermissionResponse)
def get_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    _ = Depends(check_permission("permission:read"))
):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")
    return permission

@router.delete("/permissions/{permission_id}")
def delete_permission(
    permission_id: int,
    db: Session = Depends(get_db),
    _ = Depends(check_permission("permission:delete"))
):
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")
        
    # Limpa o cache de permissões
    redis_service.delete_permission(permission_id)
        
    db.delete(permission)
    db.commit()
    return {"message": "Permissão excluída com sucesso"} 