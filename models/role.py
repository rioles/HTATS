#!/usr/bin/env python
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base


class Role(BaseModel, Base):
    __tablename__ = 'role'
    role_name = Column(String(128), unique=True, nullable=False)
    permissions = relationship('Permission', secondary='role_permissions', back_populates="roles")
    users = relationship('User', secondary='user_role', back_populates="roles")