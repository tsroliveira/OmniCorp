from sqlalchemy import Column, Integer, String, Boolean, DateTime, Table, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.backend.database.base_class import Base
from app.backend.models.user_profiles import user_profiles

# Tabela de associação entre usuários e perfis
user_profiles = Table(
    'user_profiles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('profile_id', Integer, ForeignKey('profile.id'), primary_key=True)
)

# Tabela de associação entre Profile e Permission
profile_permissions = Table(
    "profile_permissions",
    Base.metadata,
    Column("profile_id", Integer, ForeignKey("profile.id")),
    Column("permission_id", Integer, ForeignKey("permission.id"))
)

class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    level = Column(Integer, nullable=False, default=0)  # Nível hierárquico do perfil

    # Relacionamento com usuários
    users = relationship("User", secondary=user_profiles, back_populates="profiles")
    permissions = relationship("Permission", secondary=profile_permissions, back_populates="profiles")