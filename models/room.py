#!/usr/bin/env python
import sqlalchemy
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Integer, Numeric, ForeignKey, Text
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base


class RoomStatus(Enum):
    OCCUPIED = 'Occupied'
    AVAILABLE_AND_CLEAN = 'Available_and_clean'
    AVAILABLE_AND_DIRTY = 'Available_and_dirty'
    OUT_OF_ORDER = 'Out_of_order'
    

class Room(BaseModel, Base):
    __tablename__ = 'room'
    room_label = Column(String(128), unique=True, nullable=False)
    room_amount = Column(Numeric(10, 2), nullable=False)
    room_status = Column(String(128),  default=RoomStatus.AVAILABLE_AND_CLEAN.value)
    room_category_id = Column(String(60), ForeignKey('room_category.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)