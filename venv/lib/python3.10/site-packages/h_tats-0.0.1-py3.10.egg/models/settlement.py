import sqlalchemy
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Integer, Numeric, ForeignKey, Text
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base
from models.invoice import Invoice


class Settlement(BaseModel, Base):
    __tablename__ = 'settlement'
    payer_name = Column(String(128), nullable=False)
    settlement_amount =  Column(Numeric(10, 2), nullable=False)
    payer_phone = Column(String(128), nullable=True)
    invoices = relationship("Invoice", secondary="settlement_invoice", back_populates="settlements")
    payment_type_id = Column(String(60), ForeignKey('payment_type.id'), nullable=False)
    