#!/usr/bin/env python3
from datetime import datetime
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
project_dir = os.path.dirname(script_dir)
sys.path.append(project_dir)
from typing import Any, Dict, Optional, TypeVar, Union
from abc import ABC, abstractmethod
T = TypeVar('T')
class HotelReservationCrudPort(ABC):
    '''Interface for repository'''
    
    """interaacts with the MySQL database"""
    @abstractmethod
    def new(self, obj)-> None :
        """add object to current session
        """
        
    @abstractmethod
    def save(self):
        """commit current done work
        """
        
    @abstractmethod
    def find_by(self, target_class: T,  **kwargs) -> Optional[T]:
        """
        Find a object by the given criteria
        Args:
            **kwargs: The criteria to search for
        Returns:
            T: The found object_t
        """

    @abstractmethod
    def find_all_by(self, target_class: T,  **kwargs) -> T:
        """
        Find a object by the given criteria
        Args:
            **kwargs: The criteria to search for
        Returns:
            T: The found object_t
        """
    @abstractmethod
    def get_sum_with_filter(
        self, 
        target_class: T,
        sum_param1: str,
        sum_param2: str = None,
        **kwargs:Dict[str, Any]
        ):
        
        """
        Calculate the sum based on the provided sum parameters and filter conditions.
    
        Args:
            target_class (type): The class representing the database table.
            sum_param1 (str, required): The first sum parameter attribute name.
            sum_param2 (str, optional): The second sum parameter attribute name. Defaults to None.
            **kwargs: Additional filter conditions as keyword arguments.

        Returns:
            int: The calculated sum based on the sum parameters and filter conditions.
        """
   
    @abstractmethod
    def update_object(self, target_class: T, value : str, **kwargs) -> None:
        """
        Update the given object
        Args:
            value (string): The id or another attribut of the class to update
            **kwargs: The fields to update
            target_class: the class over the update is made

        Returns:
            None
        """
    @abstractmethod
    def get_all(self, target_class: T) -> T:
        """query on the current database session"""

    @abstractmethod
    def delete(self, target_obj: T):
        """delete from the current database session obj if not None
        Args
            target_object (current_object type): object that is implied in delete operation
        Return
            None if object is None else current_object
       """
    
    @abstractmethod
    def get_room_with_date_interval(
        self,
        target_class: T,
        start_date: Union[str, datetime],
        end_date: Union[str, datetime]
    ) -> list[T]:
        """
        Retrieve rooms from the database within the specified date interval.

        Args:
            target_class (Type): The class of the target objects to retrieve.
            start_date (Union[str, datetime]): The start date of the interval.
            end_date (Union[str, datetime]): The end date of the interval.

        Returns:
            list[T]: A list of objects of the specified target class within the date interval.
        """
    @abstractmethod
    def find_all_with_join(self, prim_class: T, join_class: T , **kwargs) -> T:
        """
        Find a object by the given criteria
        Args:
            **kwargs: The criteria to search for
            prim_class: mother class,
            join_class: child class
        Returns:
            T: The found object_t
        """
       
    @abstractmethod
    def close(self)-> None :
        """call remove() method on the private session attribute"""
        self.__session.remove()
        
    @abstractmethod    
    def get_sum_with_filter_and_interval(
        self, 
        target_class: T,
        sum_param1: str,
        sum_param2: str = None,
        start_date: datetime = None,
        end_date: datetime = None,
        **kwargs: Dict[str, Any]
        ) -> Any:
        """
        Calculate the sum based on the provided sum parameters and filter conditions.
    
        Args:
            target_class (Type[YourClass]): The class representing the database table.
            sum_param1 (str, required): The first sum parameter attribute name.
            sum_param2 (str, optional): The second sum parameter attribute name. Defaults to None.
            start_date (datetime, optional): The start of the day for date_column filtering.
            end_date (datetime, optional): The current date and time for date_column filtering.
            **kwargs: Additional filter conditions as keyword arguments.

        Returns:
            Any: The calculated sum based on the sum parameters and filter conditions.
        """
  


