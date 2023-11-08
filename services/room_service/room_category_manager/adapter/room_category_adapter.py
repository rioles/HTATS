
from typing import Any, Dict, Optional, TypeVar
from models.room_category import RoomCategory
from services.object_manager_interface import ObjectManagerInterface
from services.room_service.room_category_manager.port.room_category_interface import RoomCategoryPort


T = TypeVar('T')  # Type variable for the current class


class CreateCategoryRoom(RoomCategoryPort):

    def add_object(
        self,
        current_class: RoomCategory,
        **object_meta_data: Dict[str, Any]
    ) -> Optional[RoomCategory]:
        """
        Registers an object in the database.

        Args:
            current_class: Target class that add operation will be perform.
            user_object: A dictionary of properties of the user to register.

        Returns:
            The Target object , if the object was registered successfully
            and None autherwise.

        Raises:
            Exception: If the user_object dictionary is empty.
    """

        if not object_meta_data:
            raise Exception(" object_meta_data is empty.")

        try:
            current_object = RoomCategory(**object_meta_data)
            print(current_object)
            current_object.save()
        except Exception as e:
            print(e)
            return None

        return current_object
    
    def find_object_by(
        self,
        object_class: T,
        **object_meta_data:
        Dict[str, str]
    ) -> T:

        """
        Finds an object in the storage.

        Args:
            object_class: The class of the user to find.
            user_object: A criteria on which relies the user search.

        Returns:
            The user object, if found.
        """

        object_find = storage.find_by(object_class, **object_meta_data)
        return object_find
    
