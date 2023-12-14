from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar
from models import storage
from services.object_manager_interface \
    import ObjectManagerInterface


T = TypeVar('T')  # Type variable for the current class


class ObjectManagerAdapter(ObjectManagerInterface):

    def add_object(
        self,
        current_class: T,
        **object_meta_data: Dict[str, Any]
    ) -> Optional[T]:
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
            current_object = current_class(**object_meta_data)
            current_object.save()
        except Exception as e:
            print(e)
            return None

        return current_object

    # This function registers an object in the database. The `current_class`
    # argument specifies the class of the object to register.
    # The `object_meta_data `argument is a dictionary of properties of the user
    # to register. The function returns the user object, if the user was
    # registered successfully.If the object_meta_data dictionary is empty,
    # the function raises an exception. If an error occurs during registration,
    # the function also raises an exception.

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

        storage.update_object(object_class, value, **object_meta_data)

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

        all_object = {}
        objs = storage.get_all(current_class)
        if len(objs):
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                all_object[key] = obj

        return all_object
    
    def convert_object_to_dict_with_filter(self, current_class: T,**filter: Dict[str, str]) -> Dict[str, T]:

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

        all_object = {}
        objs = self.get_all_by(current_class, **filter)
        if len(objs):
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                all_object[key] = obj

        return all_object
    
    

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

        obj_dict = self.convert_object_to_dict(current_class)
        all_object = []
        
        for obj in obj_dict.values():
            all_object.append(obj.to_dict())
        return all_object
    
    def find_all_with_filter(self, current_class: T, **filter: Dict[str,Any]) -> List[Dict[str, Any]]:

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

        obj_dict = self.convert_object_to_dict_with_filter(current_class, **filter)
        all_object = []
        for obj in obj_dict.values():
            all_object.append(obj.to_dict())
        return all_object
    
    
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
        return storage.find_all_by(current_class,**filter)
    
    
    
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
        
        obj = self.find_object_by(object_class, **object_meta_data)
        if obj == None:
            return None
        obj.delete()
        return obj
    
    
    def get_all_object(self, current_class: T) -> List[T]:

        """
        get all objects of a specific class.
        This function ge all objects of a . The
        `current_class` argument specifies the class of the objects to convert.
        The function returns a dictionary of objects, where the key is the
        object's class name and the value is the object itself.

        Args:
            current_class: The class of the objects to convert.

        Returns:
            A list of current_object type.
        """

        return storage.get_all(current_class)
    
    