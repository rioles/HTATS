from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar
T = TypeVar('T')  # Type variable for the current class


class UserManagerInterface(ABC):
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

    def get_user_log(
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
    
    def find_all_users_entities(self) -> T:
        """
        Retrieve all User objects from the storage, print the type of the first user,
        and process the users using a function called return_all_user.

        Returns:
        T: Processed user data.
        """
