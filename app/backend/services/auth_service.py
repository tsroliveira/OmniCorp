from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
import logging
import traceback
import sys

from app.backend.config.settings import settings
from app.backend.config.database import get_db
from app.backend.models.user import User, Role, Permission
from app.backend.schemas.user import TokenData
from app.backend.services.ldap_service import LDAPService
from app.backend.repositories.user_repository import get_user_by_username

logger = logging.getLogger(__name__)
# Configurar logging para mostrar mais detalhes
logging.basicConfig(level=logging.DEBUG, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Configuração de hash de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Instância do serviço LDAP
ldap_service = LDAPService()

def log_exception(e: Exception, context: str = ""):
    """Registra exceção com traceback completo"""
    logger.error(f"ERRO em {context}: {str(e)}")
    logger.error(f"TRACEBACK: {''.join(traceback.format_exception(None, e, e.__traceback__))}")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    try:
        logger.debug(f"Verificando senha (hash começa com: {hashed_password[:5]}...)")
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        log_exception(e, "verify_password")
        return False

def get_password_hash(password: str) -> str:
    try:
        logger.debug("Gerando hash de senha")
        return pwd_context.hash(password)
    except Exception as e:
        log_exception(e, "get_password_hash")
        raise

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Cria um token JWT de acesso."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.auth.secret_key, algorithm=settings.auth.algorithm)
    return encoded_jwt


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Busca um usuário pelo nome de usuário."""
    return db.query(User).filter(User.username == username).first()


def get_user_permissions(db: Session, user: User) -> List[str]:
    """Obtém as permissões do usuário."""
    if not user.role_id:
        return []
    
    # Busca todas as permissões associadas ao perfil do usuário
    role_with_permissions = (
        db.query(Role)
        .filter(Role.id == user.role_id)
        .first()
    )
    
    if not role_with_permissions:
        return []
    
    permissions = []
    for role_permission in role_with_permissions.permissions:
        permission = db.query(Permission).filter(Permission.id == role_permission.permission_id).first()
        if permission:
            permissions.append(permission.name)
    
    return permissions


def authenticate_user(username: str, password: str) -> dict:
    """
    Autentica um usuário usando LDAP ou autenticação local.
    Para o usuário 'administrator', usa autenticação local.
    Para outros usuários, usa autenticação LDAP.
    
    Retorna um dicionário com:
    - username: nome do usuário
    - authenticated: booleano indicando se a autenticação foi bem sucedida
    - auth_type: "local" para administrator, "ldap" para os demais
    """
    logger.debug(f"Tentando autenticar usuário: {username}")
    try:
        # Caso especial para o administrator
        if username == "administrator":
            logger.debug("Usuário administrator detectado, usando autenticação local")
            if password == "admin@123":
                logger.info("Administrator autenticado com sucesso")
                return {
                    "username": "administrator",
                    "authenticated": True,
                    "auth_type": "local",
                    "display_name": "Administrador do Sistema",
                    "email": "admin@omnicorp.com",
                    "groups": ["Administradores"]
                }
            else:
                logger.warning("Senha incorreta para o administrator")
                return {
                    "username": "administrator",
                    "authenticated": False,
                    "auth_type": None
                }
        
        # Para outros usuários, usa LDAP
        logger.debug(f"Autenticando usuário {username} via LDAP")
        try:
            ldap_result = ldap_service.authenticate(username, password)
            logger.debug(f"Resultado da autenticação LDAP: {ldap_result}")
            
            if ldap_result:
                logger.info(f"Usuário {username} autenticado via LDAP")
                return {
                    "username": username,
                    "authenticated": True,
                    "auth_type": "ldap",
                    "display_name": username.split('@')[0],
                    "email": username,
                    "groups": ["Usuários"]
                }
            else:
                logger.warning(f"Autenticação LDAP falhou para {username}")
                return {
                    "username": username,
                    "authenticated": False,
                    "auth_type": None
                }
        except Exception as e:
            log_exception(e, f"autenticação LDAP para {username}")
            return {
                "username": username,
                "authenticated": False,
                "auth_type": None,
                "error": str(e)
            }
            
    except Exception as e:
        log_exception(e, f"autenticação do usuário {username}")
        return {
            "username": username,
            "authenticated": False,
            "auth_type": None,
            "error": str(e)
        }


def get_current_user(token: str) -> Dict[str, Any]:
    """Obtém o usuário atual a partir do token JWT."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    
    # Para simplificar, retornaremos dados básicos do usuário
    return {
        "username": username,
        "display_name": "Administrador do Sistema" if username == "administrator" else username,
        "email": "admin@omnicorp.com" if username == "administrator" else f"{username}@omnicorp.com"
    }


def get_current_active_user(current_user: Dict[str, Any] = Depends(get_current_user)):
    """Verifica se o usuário atual está ativo."""
    if not current_user.get("authenticated"):
        raise HTTPException(status_code=400, detail="Usuário inativo")
    return current_user


def create_initial_data(db: Session) -> None:
    """Cria dados iniciais no banco de dados."""
    # Criar perfis básicos
    roles = [
        {"name": "admin", "description": "Administrador do sistema"},
        {"name": "viewer", "description": "Usuário com permissões de visualização"},
        {"name": "editor", "description": "Usuário com permissões de edição"}
    ]
    
    for role_data in roles:
        role = db.query(Role).filter(Role.name == role_data["name"]).first()
        if not role:
            role = Role(**role_data)
            db.add(role)
    
    # Criar permissões básicas
    permissions = [
        {"name": "admin:all", "description": "Acesso total ao sistema"},
        {"name": "users:read", "description": "Visualizar usuários"},
        {"name": "users:write", "description": "Gerenciar usuários"},
        {"name": "modules:read", "description": "Visualizar módulos"},
        {"name": "modules:write", "description": "Gerenciar módulos"}
    ]
    
    for perm_data in permissions:
        perm = db.query(Permission).filter(Permission.name == perm_data["name"]).first()
        if not perm:
            perm = Permission(**perm_data)
            db.add(perm)
    
    # Criar usuário administrator local
    admin_user = db.query(User).filter(User.username == "administrator").first()
    if not admin_user:
        admin_role = db.query(Role).filter(Role.name == "admin").first()
        if admin_role:
            admin_user = User(
                username="administrator",
                email="admin@omnicorp.local",
                full_name="Administrador do Sistema",
                hashed_password=get_password_hash("admin@123"),
                is_ad_user=False,
                role_id=admin_role.id
            )
            db.add(admin_user)
    
    db.commit() 