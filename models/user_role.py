#!/usr/bin/env python
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base
class UserRoles(BaseModel, Base):
    __tablename__ = 'user_role'
    user_id = Column(String(60), ForeignKey('user.id', ondelete='CASCADE'))
    role_id = Column(String(60), ForeignKey('role.id', ondelete='CASCADE'))
