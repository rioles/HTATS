from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Union

from domain.room.room_entity import RoomAvailableData
T = TypeVar('T')  # Type variable for the current class


class OccupationPort(ABC):
    @abstractmethod
    def add_object(
        self,
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
    def find_object_by_intervall(
        self,
        object_class: T,
        start_date: Union[str, datetime],
        end_date: Union[str, datetime]
    ) -> T:

        """
        Finds an object in the storage.

        Args:
            object_class: The class of the user to find.
            user_object: A criteria on which relies the user search.

        Returns:
            The user object, if found.
        """
    def find_all_ivoice_by_customer(
        self
    ) -> T:
        """
        Finds all unpaid invoices associated with customers.
        Returns:
        T: The result of the operation, type may vary based on implementation.
        """
    
    @abstractmethod
    def make_payment(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        pass
    
    @abstractmethod
    def add_object_occupant(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        """
        Registers an object in the database.

        Args:
            object: A dictionary of properties of the user to register.

        Returns:
            The room_occupant object, if the room_occupant was registered successfully.

        Raises:
            Exception: If the user_object dictionary is empty.
    
    """
    
    @abstractmethod
    def get_occupation_and_room_by_invoice(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        """
        """
        
    @abstractmethod
    def update_room_status(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        """
        """
    @abstractmethod
    def get_room_entity_data(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        """
        """
    @abstractmethod    
    def vacate_room(
        self, 
        **object_meta_data: Dict[str, str]
    ) -> T:
        """
            Free up a room by deleting the room occupation and updating the room 
            status to new status.

        Parameters:
        - object_meta_data (Dict[str, str]): Metadata associated with the room to be vacated and room_occupation.
        Returns:
        - T: The room updated. 
        """
        
    def get_available_room(
        self 
    ) -> List[RoomAvailableData]:
        pass
        