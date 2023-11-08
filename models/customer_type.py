import sqlalchemy
from sqlalchemy import Column, String, DateTime, Integer
from typing import TypeVar, List, Iterable
from os import path
from datetime import datetime
from models.base import BaseModel

class CustormerType(BaseModel):
    """BasePerson class"""
    __tablename__ = 'type_custormer'
    type_custormer = Column(String(128), unique=True, nullable=False)
    
