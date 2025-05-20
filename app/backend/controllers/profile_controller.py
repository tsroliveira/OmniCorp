from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.backend.database.session import get_db
from app.backend.models.profile import Profile
from app.backend.models.permission import Permission
from app.backend.models.user import User
from app.backend.schemas.profile import ProfileCreate, ProfileUpdate, ProfileResponse
from app.backend.schemas.permission import PermissionCreate, PermissionResponse
from app.backend.middleware.auth_middleware import check_permission
from app.backend.services.redis_service import redis_service

router = APIRouter()

@router.post("/profiles", response_model=ProfileResponse)
def create_profile(
    profile: ProfileCreate,
    db: Session = Depends(get_db),
    _ = Depends(check_permission("profile:create"))
):
    db_profile = Profile(
        name=profile.name,
        description=profile.description
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile

@router.get("/profiles", response_model=List[ProfileResponse])
def list_profiles(
    db: Session = Depends(get_db),
    _ = Depends(check_permission("profile:read"))
):
    return db.query(Profile).all()

@router.get("/profiles/{profile_id}", response_model=ProfileResponse)
def get_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    _ = Depends(check_permission("profile:read"))
):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
    return profile

@router.put("/profiles/{profile_id}", response_model=ProfileResponse)
def update_profile(
    profile_id: int,
    profile: ProfileUpdate,
    db: Session = Depends(get_db),
    _ = Depends(check_permission("profile:update"))
):
    db_profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not db_profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
        
    for field, value in profile.dict(exclude_unset=True).items():
        setattr(db_profile, field, value)
        
    db.commit()
    db.refresh(db_profile)
    
    # Limpa o cache do perfil
    redis_service.delete_profile_permissions(profile_id)
    
    return db_profile

@router.delete("/profiles/{profile_id}")
def delete_profile(
    profile_id: int,
    db: Session = Depends(get_db),
    _ = Depends(check_permission("profile:delete"))
):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
        
    # Limpa o cache de permissões do perfil
    redis_service.delete_profile_permissions(profile_id)
    
    db.delete(profile)
    db.commit()
    return {"message": "Perfil excluído com sucesso"}

@router.post("/profiles/{profile_id}/permissions/{permission_id}")
def add_permission_to_profile(
    profile_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    _ = Depends(check_permission("permission:manage"))
):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
        
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")
        
    if permission not in profile.permissions:
        profile.permissions.append(permission)
        db.commit()
        
        # Limpa o cache do perfil
        redis_service.delete_profile_permissions(profile_id)
        
    return {"message": "Permissão adicionada ao perfil com sucesso"}

@router.delete("/profiles/{profile_id}/permissions/{permission_id}")
def remove_permission_from_profile(
    profile_id: int,
    permission_id: int,
    db: Session = Depends(get_db),
    _ = Depends(check_permission("permission:manage"))
):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
        
    permission = db.query(Permission).filter(Permission.id == permission_id).first()
    if not permission:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")
        
    if permission in profile.permissions:
        profile.permissions.remove(permission)
        db.commit()
        
        # Limpa o cache do perfil
        redis_service.delete_profile_permissions(profile_id)
        
    return {"message": "Permissão removida do perfil com sucesso"}

@router.post("/profiles/{profile_id}/users/{user_id}")
def add_user_to_profile(
    profile_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    _ = Depends(check_permission("permission:manage"))
):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
    if profile not in user.profiles:
        user.profiles.append(profile)
        db.commit()
        
        # Limpa o cache do usuário
        redis_service.delete_user_permissions(user_id)
        
    return {"message": "Usuário adicionado ao perfil com sucesso"}

@router.delete("/profiles/{profile_id}/users/{user_id}")
def remove_user_from_profile(
    profile_id: int,
    user_id: int,
    db: Session = Depends(get_db),
    _ = Depends(check_permission("permission:manage"))
):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil não encontrado")
        
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
        
    if profile in user.profiles:
        user.profiles.remove(profile)
        db.commit()
        
        # Limpa o cache do usuário
        redis_service.delete_user_permissions(user_id)
        
    return {"message": "Usuário removido do perfil com sucesso"} 