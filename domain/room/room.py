from dataclasses import dataclass
from typing import Optional
from domain.room.room_item_status_value_object import RoomItemStatusValueObject
from models.room import Room, RoomStatus
from models.room_category import RoomCategory
from domain.room.room_price_value_object import RoomPrice
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from domain.room.room_item_status_value_object import RoomStatusValueObject
@dataclass
class RoomEntity:
    id: str
    room: Room
    room_category: RoomCategory = Optional[RoomCategory]
    room_price: float = 0.00
    room_status: RoomStatus = Optional[RoomStatus]
    
    def __post_init__(self):
        self.room_category = self.get_category_by_id()
        self.room_price = self.get_room_price()
        self.room_status = self.get_room_status()
    
    def get_room_status(self)-> RoomStatus:
        if self.room.room_status is None:
            return None
        status: RoomStatus = RoomStatusValueObject(self.room.room_status).status
        return status    
    
    def get_category_by_id(self)->RoomCategory:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        category_room = obj.find_object_by(RoomCategory, **{"id":self.room.room_category_id})
        return category_room

    def map_room_entity_to_room_orm(self)-> Room:
        room_orm: Room = Room(
            id = self.id,
            room_status = self.room_status.value if self.room_status is not None else RoomStatus.AVAILABLE_AND_CLEAN.value,
            room_label = self.room.room_label,
            room_category_id = self.room_category.id,
            room_amount = self.room_price.price)
        
        return room_orm
    
    def get_room_price(self)-> RoomPrice:
        price: RoomPrice = RoomPrice(self.room.room_amount)
        return price
        
    def map_room_orm_to_room_entity(self)-> "RoomEntity":
        room_entity = Room(
            id = self.room.id,
            room_status = self.room_status(),
            room_category = self.room_category,
            room_amount = self.get_room_price().price)
        return room_entity
    
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        for element in my_dict:
            if element not in ["id", "room_price"]:
                my_dict[element] = my_dict[element].to_dict()
        return my_dict
                


"""
object_meta_data = {"room_label": "un label", "room_amount": 150.0, "room_category_id": "71b3b942-c8af-40f8-b3a3-b98b0c477bd2", "room_status":"Occupied"}   
objs: Room = Room(
    **object_meta_data
)
"""
object_meta_data = {"room_label": "un label", "room_amount": 150.0, "room_category_id": "71b3b942-c8af-40f8-b3a3-b98b0c477bd2"}   
objs: Room = Room(
    **object_meta_data
)
print(objs.room_status)
print(objs)
a:RoomEntity = RoomEntity(objs.id,objs)
#print(a.map_room_entity_to_room_orm())

