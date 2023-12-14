from typing import Any, Dict, List, Optional, Set, TypeVar
from domain.room.room_data import RoomData
from domain.room.room_entity import RoomDataAgregate
from models.room import Room
from models.room_item import RoomItem
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from services.room_service.room.adapter.create_room_adapter import AddRoom
from services.room_service.room.port.room_item_port import RoomItemPort
from services.room_service.room.port.room_port import RoomPort
from models import storage
T = TypeVar('T')  # Type variable for the current class


class RoomItemAdapter(RoomItemPort):
    def add_object(
        self,
        current_class: T,
        **object_meta_data: Dict[str, str]
    ) -> T:
        """
        Registers an object in the database.

        Args:
            current_class: The class of the user to register.
            user_object: A dictionary of properties of the user to register.

        Returns:
            The user object, if the user was registered successfully.

        Raises:
            Exception: If the user_object dictionary is empty.
    """
    
        object_meta_datas = self.reformat_request_data(object_meta_data)
        room_item: RoomItem = ObjectManager(object_meta_datas).create_room_item()
        room_data = self.reformat_request_data(object_meta_data)["room_data"]
        room:Room = ObjectManager(object_meta_datas).create_room()
        room_from_db:Room = get_room_by_room_label(room)
        print(room)
        try:
            
            if room_from_db is not None:
                room_data = return_room_data(room_item, object_meta_datas, room_from_db)
                room_items = room_data.map_room_item_entity_to_room_item_orm()
                room_items.save()
                return room_data.to_dict()
            else:
                rom_i: RoomPort = AddRoom()
                room_data = self.reformat_request_data(object_meta_data)["room_data"]
                room_db = rom_i.add_object(Room, **room_data)
                room_data["id"] = room_db["room"]["id"]
                object_meta_datas["room_data"] = room_data
                room:Room = ObjectManager(object_meta_datas).create_room()
                room_data = return_room_data(room_item, object_meta_datas, room)
                room_item = room_data.map_room_item_entity_to_room_item_orm()
                room_item.save()
                return room_data.to_dict()
        except Exception as e:
            print(e)
            return None

        
    
    
    def reformat_request_data(self, request_data: Dict[str, str]) -> Dict[str, Dict[str, str]]:
        """
        Reformat and preprocess the provided request data to transform it from an initial format
        to a desired format where room-related and room item-related data are organized within
        respective sub-dictionaries.

        This abstract method allows subclasses to implement custom logic for reformatting and
        organizing the input request data. It is typically used when the incoming data structure
        requires segmentation into specific categories, such as room-related and room item-related
        data.

        Parameters:
            request_data (Dict[str, str]): The input request data in its initial format.

        Returns:
            Dict[str, Dict[str, str]]: The reformatted request data in the desired format, where
            room-related and room item-related data are organized within respective sub-dictionaries.
        """
        request_data_reformat = {}
        room_item_element = {"room_item_label", "room_id", "room_status", "room_category_id"}
        room_dat_element = {"room_label", "room_amount","room_status", "room_category_id"}
        
        room_data = return_element(room_dat_element, request_data)
        room_item_data = return_element(room_item_element, request_data)     
        
        request_data_reformat["room_data"] = room_data
        request_data_reformat["room_item_data"] = room_item_data

        return request_data_reformat
    
    
      
    def find_all_object(self, current_class: T) -> List[T]:

        """
        Gets all objects of a class from the database.
        This function gets all objects of a class from the database. The
       `current_class` argument specifies the class of the objects to find.
        The function returns a list of objects, where each object is
        a dictionary of the object's properties.
        Args:
            current_class: The class of the objects to find.

        Returns:
            A list of objects.
        """
        return storage.get_all(current_class)
    
    def find_all_room_data(
        self,
        room_object: T,
        ) -> List[Dict[str, Any]]:
        """
        Retrieve all client data for a specific customer object.

        Args:
            customer_object (Type): The specific customer object for which to retrieve data.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing client data for the specified customer.

        Raises:
            Any specific exceptions raised during the data retrieval process.
        """
        all_room_items: List[Room] = storage.get_all(Room) #self.find_all_object(room_object)
        all_element:List[Dict[str, Any]] = []
        
        
        for element in all_room_items:
            room_data:RoomDataAgregate = RoomDataAgregate(element)
            all_element.append(room_data.to_dict())
        return all_element
    


        
    
    
    

def return_element(element_set: Set[str], request_data:Dict[str, str])-> Dict[str,Any]:
    data = {}
    for element in element_set:
        if element in request_data:
            data[element] = request_data[element]
    return data

    
def get_room_by_room_label(room: Room):
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    room = obj.find_object_by(Room, **{"room_label":room.room_label})
    return room

class ObjectManager:
    def __init__(self, request_data: Dict):
        self.request_data = request_data

    def create_room(self):
        room_data = self.request_data["room_data"]
        return Room(**room_data)

    def create_room_item(self):
        item_data = self.request_data["room_item_data"]
        return RoomItem(**item_data)

def return_room_data(obj1: RoomItem, object_meta_datas, obj2:Room = None):
    if obj2 is not None:
        room_data = RoomData(obj1.id, obj1, obj2)
        return room_data
    else:
        room:Room = ObjectManager(object_meta_datas).create_room()
        a = RoomData(obj1.id, obj1, room)
        return a