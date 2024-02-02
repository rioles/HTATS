from dataclasses import dataclass
from typing import Dict, List, Optional
from domain.room.room import RoomEntity
from domain.room.room_item_status_value_object import RoomItemStatusValueObject
from models.room_category import RoomCategory
from models.room import Room
from models.room_item import RoomItem, RoomItemStatus
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from models.room_item import RoomItem

@dataclass
class RoomData:
    id:str
    room_item: RoomItem
    room_orm: Room = Room
    room: RoomEntity = Optional[RoomEntity]
    __room_itme_status: RoomItemStatus = Optional[RoomItemStatus]
  
    def __post_init__(self):
        self.room = self.get_room_entity()
        self.__room_itme_status = self.room_item_status()
             
    def room_item_status(self)-> RoomItemStatus:
        if self.room_item.item_status is None:
            return None
        status: RoomItemStatus = RoomItemStatusValueObject(self.room_item.item_status).status
        return status
     
    def get_room_itmes_by_id_room(self)->List[RoomItem]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        room_item = obj.get_all_by(RoomItem, **{"id":self.room_item.room_id, })
        return room_item
     
    def get_room_entity(self):
        room_entity = RoomEntity(self.room_orm.id, self.room_orm)
        return room_entity

    def map_room_item_entity_to_room_item_orm(self)-> RoomItem:
        room_item: RoomItem = RoomItem(
            id = self.id,
            user_id = self.room_item.user_id,
            room_item_label = self.room_item.room_item_label,
            item_type = self.room_item.item_type,
            item_description = self.room_item.item_description,
            item_status = self.__room_itme_status,
            room_id = self.room_orm.id
            )
        
        return room_item
    
    def map_room_item_orm_to_room_item_entity(self)-> "RoomData":
        room_entity = RoomData(
            id = self.room_item.id,
            room_item = self.room_item,
            room = self.room if self.self.room is not None else self.get_room_entity(),
            room_itm_status = self.__room_itme_status if self.__room_itme_status is not None else RoomItemStatus.Working.value)
        return room_entity
    
        
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        keys_to_delete = {"_RoomData__room_itme_status", "room_orm","id"}
        print("this is the key", my_dict)
        
        for key in keys_to_delete.intersection(my_dict.keys()):
            del my_dict[key]
        #print(my_dict["room"].to_dict())
        for element in my_dict:
            my_dict[element] = my_dict[element].to_dict()
        return my_dict
    
    @property
    def room_itme_status(self):
        return self.__room_itme_status
    
def get_room_by_room_item(room_item: RoomItem):
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    room = obj.find_object_by(Room, **{"id":room_item.room_id})
    return room



