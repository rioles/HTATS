import sqlalchemy
from sqlalchemy import Column, String, DateTime, Integer
from typing import TypeVar, List, Iterable
from os import path
from datetime import datetime
from models.base import BaseModel
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"
class BasePerson(BaseModel):
    """BasePerson class"""
    __tablename__ = 'person'

    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)
    gender = Column(String(128), nullable=True)
    date_of_birth = Column(DateTime, nullable=True) 
    phone_number = Column(String(128), nullable=True)
    address = Column(String(128), nullable= True)
    email = Column(String(128), nullable= True)
    institute_name = Column(String(128), nullable= True)
    document_number = Column(String(128), nullable= True)
    type_of_document = Column(String(128), nullable= True)
    profession = Column(String(128), nullable= True)
    reason = Column(String(128), nullable= True)
    
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.date_of_birth = self.convert_strings_to_dates()
        
        
    def convert_strings_to_dates(self):
        if self.date_of_birth:
            self.date_of_birth = datetime.strptime(self.date_of_birth, TIMESTAMP_FORMAT)
    

