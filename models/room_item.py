#!/usr/bin/env python
import sqlalchemy
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Integer, Numeric, ForeignKey, Text
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base


class RoomItemStatus(Enum):
    WORKING = 'Working'
    NOT_WORKING= 'Not_working'
   
    

class RoomItem(BaseModel, Base):
    __tablename__ = 'room_item'
    room_item_label = Column(String(128), unique=True, nullable=False)
    item_type = Column(String(128),  nullable=True)
    item_description  = Column(Text, nullable=True)
    item_status = Column(String(128),  default=RoomItemStatus.WORKING.value)
    room_id = Column(String(60), ForeignKey('room.id'), nullable=False)
