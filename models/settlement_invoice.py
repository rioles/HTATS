#!/usr/bin/env python
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
from typing import TypeVar, List, Iterable
from models.base import BaseModel
from models.basic_base import Base


class SettlementInvoice(BaseModel, Base):
    """Class representing the doctor table"""
    __tablename__ = 'settlement_invoice'
    invoice_id = Column(String(60), ForeignKey('invoice.id'),nullable=False)
    settlement_id = Column(String(60), ForeignKey('settlement.id'), nullable=False)
    
    