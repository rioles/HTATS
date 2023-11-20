from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar
T = TypeVar('T')  # Type variable for the current class


class CustormPort(ABC):
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
        
    @abstractmethod  
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
    
    @abstractmethod
    def find_all_client_data(
        self,
        customer_object: T,
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
        pass





  

    