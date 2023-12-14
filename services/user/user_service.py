    
from typing import Any, Dict, Set
from models.employee import Employee
from models.role import Role
from models.user import User
from models.user_role import UserRoles
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from services.room_service.room.adapter.room_item_adapter import return_element


def reformat_request_data(request_data: Dict[str, str]) -> Dict[str, Dict[str, str]]:
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
    user = {"username", "email", "hashed_password", "session_id","reset_token","profil_picture"}
    employee = {"user_id","first_name", "last_name","gender", "date_of_birth","phone_number","profession"}
    role = {"role_name"}
    role_user = {"user_id","role_id"}
    user_data = return_element(user, request_data)
    employee_data = return_element(employee, request_data)
    role_data = return_element(role, request_data)
    role_user_data = return_element(role_user, request_data)   
        
    request_data_reformat["user_data"] = user_data
    request_data_reformat["employee_data"] = employee_data
    request_data_reformat["role_data"] = role_data
    request_data_reformat["role_user_data"] = role_user_data
    return request_data_reformat




class ObjectManager:
    def __init__(self, request_data: Dict):
        self.request_data = request_data

    def create_user(self):
        user_data = self.request_data["user_data"]
        return User(**user_data)

    def create_employee(self):
        employee_data = self.request_data["employee_data"]
        return Employee(**employee_data)
    
    def create_role(self):
        role_data = self.request_data["role_data"]
        return Role(**role_data)
    
    def create_role_user(self):
        role_user_data = self.request_data["role_user_data"]
        return UserRoles(**role_user_data)
