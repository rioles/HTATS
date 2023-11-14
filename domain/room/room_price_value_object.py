from dataclasses import dataclass
from decimal import Decimal, DecimalException
from typing import Union
from models.room import Room
from services.object_manager_adapter import ObjectManagerAdapter

from services.object_manager_interface import ObjectManagerInterface

@dataclass
class RoomPrice:
    __price: Union[Decimal, float] = 0.00

    def __post_init__(self):
        if not isinstance(self.__price, (float, Decimal)):
            raise ValueError("Price must be a float or Decimal")
        if self.__price < 0:
            raise ValueError("Price must be positive")
        if self.__price % 5 != 0:
            raise ValueError("Price must be a multiple of 5")

        # Convert to Decimal explicitly
        self.__price = Decimal(str(self.__price))

    @property
    def price(self):
        return self.__price

    @staticmethod
    def from_string(price_string) -> 'RoomPrice':
        try:
            price = float(price_string)
        except ValueError:
            raise ValueError("Price must be a valid number")

        if price < 0:
            raise ValueError("Price must be positive")
        if price % 5 != 0:
            raise ValueError("Price must be a multiple of 5")

        return RoomPrice(Decimal(str(price)))






object_meta_data = {"room_label": "labelsbross", "room_amount": 150.0, "room_category_id": "54ffa44e-2e0d-4c63-803d-acd8aec8d752"}   
objs: Room = Room(
    **object_meta_data
)

def get_room_by_room_label(room: Room):
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    room = obj.find_object_by(Room, **{"room_label":room.room_label})
    return room

o = get_room_by_room_label(objs)
print(o)
print(type(RoomPrice(o.room_amount).price))
print(type(RoomPrice(objs.room_amount).price))