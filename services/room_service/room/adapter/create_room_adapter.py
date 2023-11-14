from typing import Any, Dict, Optional, TypeVar
from domain.room.room import RoomEntity
from models.room import Room
from services.room_service.room.port.room_port import RoomPort
T = TypeVar('T')

class AddRoom(RoomPort):
    def add_object(self,
                 current_class: Room,
                 **object_meta_data: Dict[str, Any]
                 ) -> Optional[T]:

        try:
            room: Room = Room(**object_meta_data)
            room_entity: RoomEntity = RoomEntity(room.id, room)
            print(room_entity)
            rooms: Room = room_entity.map_room_entity_to_room_orm()
            print(rooms)
            rooms.save()
            print("this is room",room_entity.to_dict())
        except Exception as e:
            print(e)
            return None
        return room_entity.to_dict()
    
#object_meta_data = {"room_label": "unolabel", "room_amount": 2000.0, "room_category_id": "87e2a891-ea52-4aeb-b8fb-d94802d8c503"}   
  

#a: RoomPort=AddRoom()
#print(a.add_object(Room, **object_meta_data))
