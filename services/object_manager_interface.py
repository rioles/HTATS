from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar
T = TypeVar('T')  # Type variable for the current class


class ObjectManagerInterface(ABC):
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
    def update_object_in_storage(
        self,
        object_class: T,
        value: str,
        **object_meta_data:
        Dict[str, str]
    ) -> None:
        """
        Updates an object in the storage based on the specified criteria.
        This function updates an object in the storage. The `object_class`
        argument specifies the class of the object to update. The
        `value` argument specifies the value of the object to update. The
        `object_meta_data` argument is a dictionary of metadata for the object.
        The function returns the updated object.

        Args:
            object_class: The class of the object to update.
            value: The value representing the criteria
            (e.g., id or phone_number)on which the object relies for updating.
            object_meta_data: A dictionary of metadata for the object.

        Returns:
            None
            
        """
        
    def convert_object_to_dict(self, current_class: T) -> Dict[str, T]:

        """
        Converts all objects of a class to a dictionary.
        This function converts all objects of a class to a dictionary. The
        `current_class` argument specifies the class of the objects to convert.
        The function returns a dictionary of objects, where the key is the
        object's class name and the value is the object itself.

        Args:
            current_class: The class of the objects to convert.

        Returns:
            A dictionary of objects.
        """
        
    def find_all(self, current_class: T) -> List[Dict[str, Any]]:

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
    def get_all_by(self,
                current_class: T,
                **filter: Dict[str, str]
                ) -> List[Dict[str, Any]]:

        """
        Gets all objects of a class from the database.
        This function gets all objects by provided filter
        a class from the database. The
       `current_class` argument specifies the class of the objects to find.
        The function returns a list of objects, where each object is
        a dictionary of the object's properties.
        Args:
            current_class: The class of the objects to find.

        Returns:
            A list of objects.
        """
        
    
    def delete_object(
        self,
        object_class: T,
        object_meta_data: Dict[str, str],
    ) -> Optional[T]:
        """
        delete an object in the storage based on the specified criteria.
        This function delete an object in the storage. The `object_class`
        argument specifies the class of the object to delete. The
        `value` argument specifies the criteria that permit to
        get the disire object 
        `object_meta_data` argument is a dictionary of metadata for the object.
        The function returns the updated object.

        Args:
            object_class: The class of the object to update.
            value: The value representing the criteria
            (e.g., id or phone_number)on which the object relies for updating.
            

        Returns:
            None if object does not exist else object
            
        """
        