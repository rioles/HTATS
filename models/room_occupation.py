#!/usr/bin/env python
import sqlalchemy
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Integer, Numeric, ForeignKey, Text
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base
from datetime import datetime
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
    

class RoomOccupation(BaseModel, Base):
    __tablename__ = 'room_occupation'
    room_id = Column(String(60), ForeignKey('room.id'), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    invoice_id = Column(String(60), ForeignKey('invoice.id'), nullable=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.start_date, str):
            self.start_date = datetime.strptime(self.start_date, TIMESTAMP_FORMAT)
        if isinstance(self.end_date, str):
            self.end_date = datetime.strptime(self.end_date, TIMESTAMP_FORMAT)
    
    
