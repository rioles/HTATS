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
    __id:str
    __room_item: RoomItem
    __room_orm: Room = Room
    __room: RoomEntity = Optional[RoomEntity]
    __room_itme_status: RoomItemStatus = Optional[RoomItemStatus]
    
    def __post_init__(self):
        self.__room = self.get_room_entity()
        self.__room_itme_status = self.room_item_status()
              
    def room_item_status(self)-> RoomItemStatus:
        if self.__room_item.item_status is None:
            return None
        status: RoomItemStatus = RoomItemStatusValueObject(self.__room_item.item_status).status
        return status
     
    def get_room_itmes_by_id_room(self)->List[RoomItem]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        room_item = obj.get_all_by(RoomCategory, **{"id":self.__room_item.room_id, })
        return room_item
     
    def get_room_entity(self):
        room_entity = RoomEntity(self.__room_orm.id, self.__room_orm)
        return room_entity

    def map_room_item_entity_to_room_item_orm(self)-> RoomItem:
        room_item: RoomItem = RoomItem(
            id = self.__id,
            room_item_label = self.__room_item.room_item_label,
            item_type = self.__room_item.item_type,
            item_description = self.__room_item.item_description,
            item_status = self.__room_itme_status.value
            
            )
        
        return room_item
    
    def map_room_item_orm_to_room_item_entity(self)-> "RoomData":
        room_entity = RoomData(
            id = self.__room.id,
            room = self.__room,
            room_itm_status = self.__room_itme_status if self.__room_itme_status is not None else RoomItemStatus.Working.value)
        return room_entity
    
        
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        avoid_element: Dict[str,bool] = {"_RoomData__room_orm": True, "_RoomData__id": True,  "_RoomData__room_itme_status": True}

        
        for element in my_dict:
            if element not in avoid_element:
                my_dict[element] = my_dict[element].to_dict()
        return my_dict
    
    @property
    def room_itme_status(self):
        return self.__room_itme_status
    
def get_room_by_room_item(room_item: RoomItem):
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    room = obj.find_object_by(Room, **{"id":room_item.room_id})
    return room

object_meta_data = {"room_label": "un label", "room_amount": 150.0, "room_category_id": "71b3b942-c8af-40f8-b3a3-b98b0c477bd2", "room_status":"Occupied"}   
objs: Room = Room(
    **object_meta_data
)
print(objs)
objectss = {"room_item_label": "un label", "item_type": "un type", "item_description":"une dec", "room_id": objs.id}
objjj: RoomItem = RoomItem(**objectss)
print(objjj.to_dict())
#print(get_room_by_room_item(objjj))
#if get_room_by_room_item(objjj) is None:
    #a:RoomData = RoomData(objjj.id, objjj, objs)
    #print(a)
    #print(a.get_room_entity())
    #print(a.room_itme_status)
    #print(a.map_room_item_entity_to_room_item_orm())
    #print(a.to_dict())

