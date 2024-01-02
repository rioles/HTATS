from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from models.room_category import RoomCategory
from models.room import Room, RoomStatus
from models.room_occupation import RoomOccupation
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
    
@dataclass
class RoomAvailableData:
    room: Room = Room
    room_category: RoomCategory = Optional[RoomCategory]
    
    def __post_init__(self):
        self.room_category = self.get_category_by_id()
    
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



@dataclass
class RoomOccupiedData:
    room_occupation:RoomOccupation
    room: Room = Optional[Room]
    room_category: RoomCategory = Optional[RoomCategory]
    
    def __post_init__(self):
        self.room_category = self.get_category_by_id()
        self.room = self.get_room_by_category_room()
    
    def get_room_by_category_room(self)->RoomCategory:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        room = obj.find_object_by(Room, **{"id":self.room_occupation.room_id, "is_deleted":False,"room_status":RoomStatus.OCCUPIED.value})
        return room
    
    def get_category_by_id(self)->RoomCategory:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        room = self.get_room_by_category_room()
        category_room = obj.find_object_by(RoomCategory, **{"id":room.room_category_id}) if room is not None else None
        return category_room
    
    def to_dict(self):
        my_dict = dict(self.__dict__)
        key = {"room", "room_category"}
        my_object = {}
    
        for element in my_dict:
            if element is not None and element in key:
                my_object[element] = my_dict[element].to_dict()
        return my_object
    
  

        

