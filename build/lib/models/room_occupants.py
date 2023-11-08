#!/usr/bin/env python
import sqlalchemy
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
from typing import TypeVar, List, Iterable
from models.base_person import BasePerson
from models.basic_base import Base


class RoomOccupants(BasePerson, Base):
    """Class representing the doctor table"""
    __tablename__ = 'room_occupants'
    occupation_id = Column(String(60), ForeignKey('room_occupation.id'), nullable=False)

    