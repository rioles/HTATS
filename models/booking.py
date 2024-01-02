import sqlalchemy
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Integer, Numeric, ForeignKey, Text
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base
from datetime import datetime
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

class BookingStatus(Enum):
    CONFIRMED = 'Confirmed'
    PENDING = 'Pending'
    CANCELLED = 'Cancelled'
    PROGRESS = 'progress'

class Booking(BaseModel, Base):
    __tablename__ = 'booking'
    booking_status = Column(String(128), nullable=False)
    booking_price =  Column(Numeric(10, 2), nullable=False)
    start_date =  Column(DateTime)
    end_date = Column(DateTime)
    invoice_id = Column(String(60), ForeignKey('invoice.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if isinstance(self.start_date, str):
            self.start_date = datetime.strptime(self.start_date, TIMESTAMP_FORMAT)
        if isinstance(self.end_date, str):
            self.end_date = datetime.strptime(self.end_date, TIMESTAMP_FORMAT)
    