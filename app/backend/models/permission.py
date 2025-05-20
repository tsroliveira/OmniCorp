from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.backend.database.base_class import Base

class Permission(Base):
    __tablename__ = "permission"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(String(255))
    
    # Relacionamento com perfis
    profiles = relationship("Profile", secondary="profile_permissions", back_populates="permissions") 