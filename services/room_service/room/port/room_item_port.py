from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar
T = TypeVar('T')  # Type variable for the current class


class RoomItemPort(ABC):
    @abstractmethod
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
    
    @abstractmethod
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
        pass

        