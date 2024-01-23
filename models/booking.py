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
    COMPLETE= 'Complete'

class Booking(BaseModel, Base):
    __tablename__ = 'booking'
    booking_status = Column(String(128), nullable=False)
    booking_price =  Column(Numeric(10, 2), nullable=True)
    room_id = Column(String(60), ForeignKey('room.id'), nullable=False)
    percentage =  Column(Numeric(10, 2), nullable=True)
    start_date =  Column(DateTime)
    end_date = Column(DateTime)
    invoice_id = Column(String(60), ForeignKey('invoice.id'), nullable=True)
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.start_date = self.start_date.strftime(TIMESTAMP_FORMAT)
        #self.end_date = self.end_date.strftime(TIMESTAMP_FORMAT)
        #self.convert_dates_to_string()
        #self.end_date = datetime.strptime(self.end_date, TIMESTAMP_FORMAT)
        
    def convert_dates_to_string(self):
        if self.start_date and isinstance(self.start_date, datetime):
            self.start_date = self.start_date.strftime(TIMESTAMP_FORMAT)
            #self.start_date = datetime.strptime(self.start_date, TIMESTAMP_FORMAT)
        if self.end_date and isinstance(self.end_date, datetime):
            self.end_date = self.end_date.strftime(TIMESTAMP_FORMAT)
            #self.end_date = datetime.strptime(self.end_date, TIMESTAMP_FORMAT)
            
    def convert_strings_to_dates(self):
        if self.start_date and isinstance(self.start_date, str):
            self.start_date = datetime.strptime(self.start_date, TIMESTAMP_FORMAT)
        if self.end_date and isinstance(self.end_date, str):
            self.end_date = datetime.strptime(self.end_date, TIMESTAMP_FORMAT)
    