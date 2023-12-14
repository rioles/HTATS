#!/usr/bin/env python
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base
class RolePermissions(BaseModel, Base):
    __tablename__ = 'role_permissions'
    permission_id = Column(String(60), ForeignKey('permission.id', ondelete='CASCADE'))
    role_id = Column(String(60), ForeignKey('role.id', ondelete='CASCADE'))
