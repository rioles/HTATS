import sqlalchemy
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Integer, Numeric, ForeignKey, Text
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base
from models.invoice import Invoice
from sqlalchemy import Column, String, DateTime
from datetime import datetime


class LoginHistory(BaseModel, Base):
    __tablename__ = 'login_history'
    logout_timestamp = Column(DateTime, default=datetime.utcnow)
    login_timestamp =  Column(DateTime, nullable=False)
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
