from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.backend.database.session import get_db
from app.backend.models.user import User
from app.backend.models.profile import Profile
from app.backend.models.permission import Permission
from app.backend.services.auth_service import decode_token
from app.backend.services.redis_service import redis_service
from typing import List, Set

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        token = credentials.credentials
        payload = decode_token(token)
        username = payload.get("sub")
        
        if not username:
            raise HTTPException(status_code=401, detail="Token inválido")
            
        user = db.query(User).filter(User.username == username).first()
        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")
            
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def check_permission(permission_name: str):
    def permission_checker(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
        # Verifica se o usuário tem o perfil de administrador
        if any(profile.name == "Administrador" for profile in user.profiles):
            return user
            
        # Tenta obter as permissões do cache
        cached_permissions = redis_service.get_user_permissions(user.id)
        if cached_permissions and permission_name in cached_permissions:
            return user
            
        # Se não estiver no cache, busca do banco de dados
        user_permissions = set()
        for profile in user.profiles:
            # Tenta obter as permissões do perfil do cache
            cached_profile_permissions = redis_service.get_profile_permissions(profile.id)
            if cached_profile_permissions:
                user_permissions.update(cached_profile_permissions)
            else:
                # Se não estiver no cache, busca do banco de dados
                profile_permissions = {p.name for p in profile.permissions}
                user_permissions.update(profile_permissions)
                # Armazena no cache
                redis_service.set_profile_permissions(profile.id, list(profile_permissions))
        
        # Armazena as permissões do usuário no cache
        redis_service.set_user_permissions(user.id, list(user_permissions))
        
        if permission_name in user_permissions:
            return user
            
        raise HTTPException(
            status_code=403,
            detail=f"Usuário não tem permissão para acessar este recurso. Permissão necessária: {permission_name}"
        )
    return permission_checker

# Permissões predefinidas
PERMISSIONS = {
    "admin": "Acesso total ao sistema",
    "user:create": "Criar usuários",
    "user:read": "Visualizar usuários",
    "user:update": "Atualizar usuários",
    "user:delete": "Excluir usuários",
    "profile:create": "Criar perfis",
    "profile:read": "Visualizar perfis",
    "profile:update": "Atualizar perfis",
    "profile:delete": "Excluir perfis",
    "permission:manage": "Gerenciar permissões"
} 