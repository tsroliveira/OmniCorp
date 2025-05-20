from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.backend.config.database import get_db
from app.backend.models.user import User, Role
from app.backend.schemas.user import User as UserSchema, UserCreate, UserUpdate, Role as RoleSchema
from app.backend.services.auth_service import (
    get_current_active_user, 
    get_password_hash, 
    get_user_permissions
)
from app.backend.middleware.auth_middleware import check_permission
from app.backend.services.redis_service import redis_service

router = APIRouter(
    prefix="/api/users",
    tags=["users"],
    responses={401: {"description": "Não autorizado"}},
)


def check_admin_permission(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Verifica se o usuário tem permissão de administrador."""
    permissions = get_user_permissions(db, current_user)
    if "admin:all" not in permissions and current_user.username != "administrator":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada para esta operação",
        )
    return current_user


@router.get("/", response_model=List[UserSchema])
async def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permission)
):
    """Retorna a lista de usuários."""
    users = db.query(User).offset(skip).limit(limit).all()
    return users


@router.get("/{user_id}", response_model=UserSchema)
async def read_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permission)
):
    """Retorna um usuário específico pelo ID."""
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return user


@router.post("/", response_model=UserSchema)
async def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permission)
):
    """Cria um novo usuário local."""
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já registrado")
    
    # Verifica o perfil padrão (viewer)
    viewer_role = db.query(Role).filter(Role.name == "viewer").first()
    if not viewer_role:
        raise HTTPException(status_code=500, detail="Perfil padrão 'viewer' não encontrado")
    
    hashed_password = get_password_hash(user.password) if user.password else None
    
    new_user = User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password,
        is_ad_user=False,
        is_active=user.is_active,
        role_id=viewer_role.id
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Limpa o cache de permissões do usuário
    redis_service.delete_user_permissions(new_user.id)
    
    return new_user


@router.put("/{user_id}", response_model=UserSchema)
async def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permission)
):
    """Atualiza um usuário existente."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Atualiza os campos
    if user_update.email is not None:
        db_user.email = user_update.email
    if user_update.full_name is not None:
        db_user.full_name = user_update.full_name
    if user_update.is_active is not None:
        db_user.is_active = user_update.is_active
    if user_update.role_id is not None:
        # Verifica se o perfil existe
        role = db.query(Role).filter(Role.id == user_update.role_id).first()
        if not role:
            raise HTTPException(status_code=400, detail="Perfil inválido")
        db_user.role_id = user_update.role_id
    
    db.commit()
    db.refresh(db_user)
    
    # Limpa o cache de permissões do usuário
    redis_service.delete_user_permissions(db_user.id)
    
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permission)
):
    """Remove um usuário."""
    # Impede a exclusão do usuário administrador
    if current_user.id == user_id or user_id == 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Não é possível excluir este usuário"
        )
    
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    # Limpa o cache de permissões do usuário
    redis_service.delete_user_permissions(db_user.id)
    
    db.delete(db_user)
    db.commit()
    return None


@router.get("/roles/", response_model=List[RoleSchema])
async def read_roles(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retorna a lista de perfis disponíveis."""
    roles = db.query(Role).all()
    return roles 