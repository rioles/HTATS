import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base
from flask_login import UserMixin

class User(UserMixin, BaseModel, Base):
    __tablename__ = 'user'
    username = Column(String(128), unique=True, nullable=True)
    email = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
    profil_picture = Column(String(128), nullable=True)
    roles = relationship('Role', secondary='user_role', back_populates="users")
    
    
    