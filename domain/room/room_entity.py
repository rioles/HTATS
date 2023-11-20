from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from domain.room.room import RoomEntity
from domain.room.room_item_status_value_object import RoomItemStatusValueObject
from models.room_category import RoomCategory
from models.room import Room
from models.room_item import RoomItem, RoomItemStatus
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from models.room_item import RoomItem

@dataclass
class RoomDataAgregate:
    room: Room = Room
    room_item: List[Dict[str, Any]] = field(default_factory=list)
    room_category: RoomCategory = Optional[RoomCategory]
    
    def __post_init__(self):
        self.room_item = self.get_all_itme_by_room()
        self.room_category = self.get_category_by_id()
        
    def get_all_itme_by_room(self):
        obj:ObjectManagerInterface = ObjectManagerAdapter()
        all_items = obj.find_all_with_filter(RoomItem, **{"room_id":self.room.id})
        #print("this is all_item", all_items)
        return all_items
    
    def get_category_by_id(self)->RoomCategory:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        category_room = obj.find_object_by(RoomCategory, **{"id":self.room.room_category_id})
        return category_room
    
    def to_dict(self):
        my_dict = dict(self.__dict__)
        key = {"room", "room_category"}
        my_object = {}
    
        for element in my_dict:
            if element in key and element is not None:
                print(my_dict[element].to_dict())
                my_object[element] = my_dict[element].to_dict()
            if element == "room_item":
                my_object[element] = my_dict[element]
        return my_object
        

