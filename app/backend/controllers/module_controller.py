from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.backend.config.database import get_db
from app.backend.models.user import Module, Permission, User
from app.backend.schemas.user import Module as ModuleSchema, ModuleCreate
from app.backend.services.auth_service import (
    get_current_active_user, 
    get_user_permissions
)

router = APIRouter(
    prefix="/api/modules",
    tags=["modules"],
    responses={401: {"description": "Não autorizado"}},
)


def check_admin_permission(current_user: User = Depends(get_current_active_user), db: Session = Depends(get_db)):
    """Verifica se o usuário tem permissão de administrador."""
    permissions = get_user_permissions(db, current_user)
    if "admin:all" not in permissions and "modules:write" not in permissions:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permissão negada para esta operação",
        )
    return current_user


@router.get("/", response_model=List[ModuleSchema])
async def read_modules(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Retorna todos os módulos disponíveis."""
    # Obtém as permissões do usuário
    user_permissions = get_user_permissions(db, current_user)
    
    # Se for admin, retorna todos os módulos
    if "admin:all" in user_permissions:
        return db.query(Module).filter(Module.is_active == True).all()
    
    # Caso contrário, filtra por permissões
    accessible_modules = []
    modules = db.query(Module).filter(Module.is_active == True).all()
    
    for module in modules:
        permission = db.query(Permission).filter(Permission.id == module.required_permission_id).first()
        if permission and permission.name in user_permissions:
            accessible_modules.append(module)
    
    return accessible_modules


@router.post("/", response_model=ModuleSchema)
async def create_module(
    module: ModuleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permission)
):
    """Cria um novo módulo."""
    # Verifica se o nome do módulo já existe
    db_module = db.query(Module).filter(Module.name == module.name).first()
    if db_module:
        raise HTTPException(status_code=400, detail="Nome do módulo já existe")
    
    # Verifica se a permissão existe
    permission = db.query(Permission).filter(Permission.id == module.required_permission_id).first()
    if not permission:
        raise HTTPException(status_code=400, detail="Permissão não encontrada")
    
    # Cria o novo módulo
    new_module = Module(
        name=module.name,
        description=module.description,
        url=module.url,
        icon=module.icon,
        is_active=module.is_active,
        required_permission_id=module.required_permission_id
    )
    
    db.add(new_module)
    db.commit()
    db.refresh(new_module)
    return new_module


@router.put("/{module_id}", response_model=ModuleSchema)
async def update_module(
    module_id: int, 
    module_data: ModuleCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permission)
):
    """Atualiza um módulo existente."""
    db_module = db.query(Module).filter(Module.id == module_id).first()
    if not db_module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    
    # Verifica se o nome já existe em outro módulo
    name_exists = db.query(Module).filter(Module.name == module_data.name, Module.id != module_id).first()
    if name_exists:
        raise HTTPException(status_code=400, detail="Nome do módulo já existe")
    
    # Verifica se a permissão existe
    permission = db.query(Permission).filter(Permission.id == module_data.required_permission_id).first()
    if not permission:
        raise HTTPException(status_code=400, detail="Permissão não encontrada")
    
    # Atualiza os campos
    db_module.name = module_data.name
    db_module.description = module_data.description
    db_module.url = module_data.url
    db_module.icon = module_data.icon
    db_module.is_active = module_data.is_active
    db_module.required_permission_id = module_data.required_permission_id
    
    db.commit()
    db.refresh(db_module)
    return db_module


@router.delete("/{module_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_module(
    module_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(check_admin_permission)
):
    """Remove um módulo existente."""
    db_module = db.query(Module).filter(Module.id == module_id).first()
    if not db_module:
        raise HTTPException(status_code=404, detail="Módulo não encontrado")
    
    db.delete(db_module)
    db.commit()
    return None 