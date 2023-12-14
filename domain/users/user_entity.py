from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional
from models.customer_type import CustormerType
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from models.user import User
from models.employee import Employee
from models.role import Role
from models.user_role import UserRoles
from models.invoice import Invoice, InvoiceStatus
from models import storage


@dataclass
class UserEntity:
    user: User
    employee:Employee = Optional[Employee]
    role:Role = field(default_factory=list)

    
    def __post_init__(self):
        self.employee = self.get_employee_user_id()
        self.role = self.get_roles_by_user()

    
    def get_employee_user_id(self)->Employee:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        user = self.user
        employee = obj.find_object_by(Employee, **{"user_id":user.id})
        return employee
    
    
    def get_roles_by_user(self)->List[Role]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        role_users = obj.get_all_by(UserRoles, **{"user_id": self.user.id})
        role_ids = [role_user.role_id for role_user in role_users]
        roles = list(map(lambda role_id: obj.find_object_by(Role, **{"id": role_id}), role_ids))
        roles_as_dicts = list(map(lambda role: role.to_dict(), roles))
        return roles_as_dicts
    
    
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        print(my_dict)
        keys = {"user", "employee"} 
        for key in my_dict:
            if key in keys and key is not None:
                my_dict[key] = my_dict[key].to_dict()
            else:
                my_dict[key] = my_dict[key]
        return my_dict
                
        