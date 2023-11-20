from dataclasses import dataclass
from decimal import Decimal, DecimalException
from typing import Union
from models.room import Room
from services.object_manager_adapter import ObjectManagerAdapter

from services.object_manager_interface import ObjectManagerInterface
from dataclasses import dataclass
from decimal import Decimal


@dataclass
class RoomPrice:
    __price: Decimal = 0.00

    def _validate_positive_and_multiple_of_5(self, price):
        if price < 0:
            raise ValueError("Price must be positive")
        if price % 5 != 0:
            raise ValueError("Price must be a multiple of 5")

    def _validate_and_set_price(self, price):
        if isinstance(price, Decimal):
            self._validate_positive_and_multiple_of_5(price)
            self.__price = price
        elif isinstance(price, float):
            # Convert float to Decimal
            self.__price = Decimal(str(price))
            self._validate_positive_and_multiple_of_5(self.__price)
        elif isinstance(price, str):
            try:
                # Try parsing the string as a float
                float_price = float(price)
            except ValueError:
                raise ValueError("Price must be a valid number")

            # Validate the float price
            self._validate_positive_and_multiple_of_5(float_price)

            # Convert the valid float to Decimal
            self.__price = Decimal(str(float_price))
        else:
            raise ValueError("Price must be a Decimal, float, or a valid number string")

    def __post_init__(self):
        self._validate_and_set_price(self.__price)

    @property
    def price(self):
        return self.__price

    @staticmethod
    def from_string(price_string) -> 'RoomPrice':
        room_price = RoomPrice()
        room_price._validate_and_set_price(price_string)
        return room_price




object_meta_data = {"room_label": "labelsbross", "room_amount": "150.0", "room_category_id": "54ffa44e-2e0d-4c63-803d-acd8aec8d752"}   
objs: Room = Room(
    **object_meta_data
)

def get_room_by_room_label(room: Room):
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    room = obj.find_object_by(Room, **{"room_label":room.room_label})
    return room


c:RoomPrice = RoomPrice("150.00")
f:RoomPrice = RoomPrice(150.00)
print(c)

