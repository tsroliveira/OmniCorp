from sqlalchemy import Column, Integer, ForeignKey, Table
from app.backend.database.base_class import Base

profile_permissions = Table(
    'profile_permissions',
    Base.metadata,
    Column('profile_id', Integer, ForeignKey('profile.id'), primary_key=True),
    Column('permission_id', Integer, ForeignKey('permission.id'), primary_key=True)
) 