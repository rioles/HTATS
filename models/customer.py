#!/usr/bin/env python
from datetime import datetime
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
from typing import TypeVar, List, Iterable
from models.base_person import BasePerson
from models.basic_base import Base



class Customer(BasePerson, Base):
    """Class representing the doctor table"""
    __tablename__ = 'customer'
    ifu = Column(String(128), nullable=True)
    customer_invoice = relationship("Invoice", backref="Customer", cascade="delete")
    customer_type_id = Column(String(60), ForeignKey('type_custormer.id'), nullable=False)
    invoices = relationship('Invoice', back_populates='customer')
    user_id = Column(String(60), ForeignKey('user.id'), nullable=False)
    
    
    