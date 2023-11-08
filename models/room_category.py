#!/usr/bin/env python
import sqlalchemy
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Integer, Numeric, ForeignKey, Text
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base



class RoomCategory(BaseModel, Base):
    __tablename__ = 'room_category'
    room_category_label = Column(String(128), unique=True, nullable=False)
    place_number = Column(String(128), nullable=False)
    rooms = relationship('Room', backref='category')