from typing import Any, Dict, List, Optional, TypeVar
from models.room import Room
from models.room_item import RoomItem
from services.room_service.room.port.room_item_port import RoomItemPort
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
        room_data = {"room_label":request_data["room_label"], "room_amount":request_data["room_amount"],
                     "room_status": request_data["room_status"], "room_category_id":request_data["room_category_id"]
                    }
        
        room_item_data = {"room_item_label": request_data["room_item_label"], "room_id":request_data["room_id"]}
        
        request_data_reformat["room_data"] = room_data
        request_data_reformat["room_item_data"] = room_item_data

        return request_data_reformat
    

class ObjectManager:
    def __init__(self, request_data: Dict):
        self.request_data = request_data

    def create_room(self):
        room_data = self.request_data["room_data"]
        return Room(**room_data)

    def create_room_item(self):
        item_data = self.request_data["room_item_data"]
        return RoomItem(**item_data)