#!/usr/bin/env python
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base


class TokenBlockList(BaseModel, Base):
    __tablename__ = 'token_block_list'
    jti = Column(String(128), unique=True, nullable=False)
