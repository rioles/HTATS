import sqlalchemy
from sqlalchemy import Column, String, DateTime, Integer
from typing import TypeVar, List, Iterable
from os import path
from datetime import datetime
from models.base import BaseModel

class BasePerson(BaseModel):
    """BasePerson class"""
    __tablename__ = 'person'

    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    gender = Column(String(128), nullable=True)
    date_of_birth = Column(DateTime, nullable=True) # look at this date later
    phone_number = Column(String(128), nullable=True)
    address = Column(String(128), nullable= True)
    

