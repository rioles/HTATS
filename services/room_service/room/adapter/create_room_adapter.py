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
            print(room)
            rooms: Room = room_entity.map_room_entity_to_room_orm()
            print(rooms)
            rooms.save()
            print(room_entity.to_dict())
        except Exception as e:
            print(e)
            return None
        return room_entity.to_dict()
    
    


