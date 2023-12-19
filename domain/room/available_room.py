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
class RoomData:
    id:str
    numbe_of_room: int
    room: Room = field(default_factory=list)
    
    
    def get_all_itme_by_room(self):
        obj:ObjectManagerInterface = ObjectManagerAdapter()
        room = obj.find_all(Room)
        return room
    
    def get_number_of_room(self):
        number_of_room = len(self.get_all_itme_by_room)
        return number_of_room
    