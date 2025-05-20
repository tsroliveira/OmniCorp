from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from app.backend.database.base_class import Base

# Tabela de associação entre usuários e perfis
user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True)
)

class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Relacionamento com usuários
    users = relationship('User', secondary=user_roles, back_populates='roles')

class Permission(Base):
    __tablename__ = 'permission'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)

    # Relacionamento com perfis
    roles = relationship('Role', secondary='role_permissions', back_populates='permissions')

# Tabela de associação entre perfis e permissões
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True)
) 