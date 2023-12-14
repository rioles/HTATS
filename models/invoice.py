#!/usr/bin/env python
import sqlalchemy
from enum import Enum
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, DateTime, Integer, Numeric, ForeignKey, Text
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base


class InvoiceStatus(Enum):
    PAID = 'Paid'
    UNPAID = 'Unpaid'
    CANCELLED = 'Cancelled'
    

class Invoice(BaseModel, Base):
    __tablename__ = 'invoice'
    invoice_number = Column(String(128), unique=True, nullable=False)
    invoice_amount =  Column(Numeric(10, 2), nullable=False)
    invoice_status = Column(String(128), nullable=True)
    customer_id = Column(String(60), ForeignKey('customer.id'), nullable=False)
    settlements = relationship("Settlement", secondary="settlement_invoice", back_populates="invoices")
    customer = relationship('Customer', back_populates='invoices')