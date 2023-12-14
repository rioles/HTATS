#!/usr/bin/env python
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
from typing import TypeVar, List, Iterable
from models.basic_base import Base
from models.base import BaseModel

class Permission(BaseModel, Base):
    __tablename__ = 'permission'
    name = Column(String(128), unique=True, nullable=False)
    roles= relationship('Role', secondary='role_permissions', back_populates="permissions")