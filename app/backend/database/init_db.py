from sqlalchemy.orm import Session
from app.backend.database.base_class import Base
from app.backend.database.session import engine
from app.backend.models.user import User
from app.backend.models.profile import Profile
from app.backend.models.permission import Permission
from app.backend.database.session import get_db

def init_db():
    # Criar todas as tabelas
    Base.metadata.create_all(bind=engine)
    
    # Obter sessão do banco de dados
    db = next(get_db())
    
    try:
        # Criar permissões básicas
        permissions = [
            Permission(name="view_users", description="Visualizar usuários"),
            Permission(name="create_users", description="Criar usuários"),
            Permission(name="edit_users", description="Editar usuários"),
            Permission(name="delete_users", description="Deletar usuários"),
            Permission(name="view_profiles", description="Visualizar perfis"),
            Permission(name="manage_profiles", description="Gerenciar perfis"),
            Permission(name="view_permissions", description="Visualizar permissões"),
            Permission(name="manage_permissions", description="Gerenciar permissões")
        ]
        
        for permission in permissions:
            if not db.query(Permission).filter(Permission.name == permission.name).first():
                db.add(permission)
        
        db.commit()
        
        # Criar perfis básicos
        admin_profile = Profile(
            name="Administrador",
            description="Perfil com acesso total ao sistema"
        )
        db.add(admin_profile)
        db.commit()
        
        # Adicionar todas as permissões ao perfil de administrador
        for permission in permissions:
            admin_profile.permissions.append(permission)
        
        db.commit()
        
        # Atualizar usuário admin para usar o perfil de administrador
        admin_user = db.query(User).filter(User.username == "admin").first()
        if admin_user:
            admin_user.profile = admin_profile
            db.commit()
            
        print("Banco de dados inicializado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db() 