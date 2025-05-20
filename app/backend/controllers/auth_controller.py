from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Dict, Any
from jose import JWTError, jwt
import logging
import traceback

from app.backend.config.database import get_db
from app.backend.config.settings import settings
from app.backend.services.auth_service import (
    authenticate_user,
    create_access_token,
    get_current_active_user,
    get_user_permissions
)
from app.backend.models.user import User
from app.backend.schemas.user import Token, User as UserSchema

# Configurar logging
logger = logging.getLogger(__name__)

# Definindo o endpoint de autenticação
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token")

router = APIRouter(
    prefix="/api/auth",
    tags=["auth"],
    responses={401: {"description": "Não autorizado"}},
)

def log_exception(e: Exception, context: str = ""):
    """Registra exceção com traceback completo"""
    logger.error(f"ERRO no controlador de auth em {context}: {str(e)}")
    logger.error(f"TRACEBACK: {''.join(traceback.format_exception(None, e, e.__traceback__))}")

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """Endpoint para obter token de acesso via login."""
    logger.debug(f"Tentativa de login para usuário: {form_data.username}")
    try:
        logger.debug("Chamando authenticate_user")
        auth_result = authenticate_user(form_data.username, form_data.password)
        logger.debug(f"Resultado da autenticação: {auth_result}")
        
        if not auth_result or not auth_result.get("authenticated", False):
            logger.warning(f"Falha na autenticação para usuário: {form_data.username}")
            error_message = auth_result.get("error", "Nome de usuário ou senha incorretos") if auth_result else "Nome de usuário ou senha incorretos"
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=error_message,
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        logger.info(f"Usuário {form_data.username} autenticado com sucesso via {auth_result.get('auth_type')}")
        
        # Cria o payload do token
        logger.debug("Criando token de acesso")
        expire_minutes = int(settings.auth.access_token_expire_minutes)
        access_token_expires = timedelta(minutes=expire_minutes)
        access_token = create_access_token(
            data={
                "sub": auth_result["username"],
                "permissions": ["admin:all"] if auth_result["username"] == "administrator" else ["user:read"]
            },
            expires_delta=access_token_expires
        )
        logger.debug(f"Token criado para usuário {form_data.username}")
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "username": auth_result["username"],
                "display_name": auth_result.get("display_name", auth_result["username"]),
                "email": auth_result.get("email", f"{auth_result['username']}@omnicorp.com"),
                "groups": auth_result.get("groups", ["Usuários"])
            }
        }
    except HTTPException as he:
        # Repassa exceções HTTP
        raise he
    except Exception as e:
        log_exception(e, f"login para {form_data.username}")
        logger.error(f"Erro não tratado durante login: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno durante autenticação",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.get("/me")
async def read_users_me(
    token: str = Depends(oauth2_scheme)
):
    """Retorna informações do usuário atual."""
    logger.debug("Solicitação para /me recebida")
    try:
        # Decodifica o token
        logger.debug("Decodificando token JWT")
        payload = jwt.decode(token, settings.auth.secret_key, algorithms=[settings.auth.algorithm])
        username = payload.get("sub")
        logger.debug(f"Token decodificado para usuário: {username}")
        
        # Retorna as informações do usuário
        user_info = {
            "username": username,
            "display_name": "Administrador do Sistema" if username == "administrator" else username,
            "email": "admin@omnicorp.com" if username == "administrator" else f"{username}@omnicorp.com",
            "groups": payload.get("groups", ["Usuários"])
        }
        logger.debug(f"Retornando informações do usuário: {user_info}")
        return user_info
    except JWTError as e:
        logger.error(f"Erro JWT: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        log_exception(e, "endpoint /me")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao processar o token",
            headers={"WWW-Authenticate": "Bearer"},
        ) 