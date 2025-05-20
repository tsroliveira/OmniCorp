from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from app.backend.database.base_class import Base
from app.backend.models.user_profiles import user_profiles


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    full_name = Column(String(255))
    hashed_password = Column(String(255), nullable=True)  # Somente para o usuário administrator
    is_active = Column(Boolean, default=True)
    is_ad_user = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    profile_id = Column(Integer, ForeignKey("profile.id"))

    # Relacionamento com perfis
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role", back_populates="users")

    # Relacionamentos
    profiles = relationship("Profile", secondary=user_profiles, back_populates="users")
    profile = relationship("Profile", back_populates="users")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(255))
    
    # Relacionamento com usuários
    users = relationship("User", back_populates="role")
    
    # Relacionamento com permissões
    permissions = relationship("RolePermission", back_populates="role")


class Permission(Base):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(255))
    
    # Relacionamento com perfis
    roles = relationship("RolePermission", back_populates="permission")


class RolePermission(Base):
    __tablename__ = "role_permissions"
    
    id = Column(Integer, primary_key=True, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    permission_id = Column(Integer, ForeignKey("permissions.id"))
    
    # Relacionamentos
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission", back_populates="roles")


class Module(Base):
    __tablename__ = "modules"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(255))
    url = Column(String(255))
    icon = Column(String(50))
    is_active = Column(Boolean, default=True)
    
    # Relacionamento com permissões
    required_permission_id = Column(Integer, ForeignKey("permissions.id"))
    required_permission = relationship("Permission") 