from sqlalchemy import Table, Column, Integer, ForeignKey
from app.backend.database.base_class import Base

# Tabela de associação entre User e Profile
user_profiles = Table(
    "user_profiles",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id"), primary_key=True),
    Column("profile_id", Integer, ForeignKey("profile.id"), primary_key=True)
) 