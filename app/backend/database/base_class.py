from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Importar todos os modelos aqui para que o Alembic possa encontrá-los
from app.backend.models.user import User
from app.backend.models.profile import Profile
from app.backend.models.permission import Permission
from app.backend.models.profile_permission import profile_permissions 