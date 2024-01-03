from typing import Any, Dict, TypeVar, List
from domain.users.user_entity import UserEntity
from models.login_history import LoginHistory
from models.role import Role
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from bcrypt import hashpw, gensalt, checkpw
from services.user.user_port import UserManagerInterface
from services.user.user_service import ObjectManager, reformat_request_data
from models.user import User
from models import storage
from models.user_role import UserRoles
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from models.employee import Employee

T = TypeVar('T')

class UserAdapter(UserManagerInterface):
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

        object_meta_data["hashed_password"] = _hash_password(object_meta_data["hashed_password"]).decode('utf-8')
        object_meta_datas = reformat_request_data(object_meta_data)
        create_object: ObjectManager = ObjectManager(object_meta_datas)
        print("metadata", object_meta_datas["role_data"])
        obj:ObjectManagerInterface = ObjectManagerAdapter()
        role = obj.find_object_by(Role, **{"role_name":object_meta_datas["role_data"]["role_name"]})
        role_obj = create_object.create_role()   
        user_obj = create_object.create_user()
        object_meta_data["user_id"] = user_obj.id
        object_meta_data["role_id"] = role_obj.id if role is None else role.id
        data = reformat_request_data(object_meta_data)
        create_object: ObjectManager = ObjectManager(data)
        employee_obj = create_object.create_employee()
        user_role_obj = create_object.create_role_user()


        try:
            all_object = {} 
            user_obj.save()
            if role is None:
                role_obj.save()
            employee_obj.save()
            user_role_obj.save()
            all_object["user"] = user_obj.to_dict()
            all_object["role"] = role_obj.to_dict() if role is None else role.to_dict()
            all_object["employee"] = employee_obj.to_dict()
            all_object["user_role"] = user_role_obj.to_dict()
            print("all_obj", all_object)
            return all_object
        except Exception as e:
            print(e)
            return None

      
        
    
    def get_user_log(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        
        user = storage.find_by(User, **{"email":object_meta_data["email"]})
        print("user", user)
        if user is not None and valid_login(user, object_meta_data["hashed_password"]):
            user_role = storage.find_by(UserRoles, **{"user_id":user.id})
            role = storage.find_by(Role, **{"id":user_role.role_id})
            employee = storage.find_by(Employee, **{"user_id":user.id})
            return {"user": user.to_dict(), "role":role.to_dict(), "employee":employee.to_dict()}
        else:
            return None
    
    def find_all_users_entities(
        self
    ) -> T:
        
        users = storage.get_all(User)
        print(users)
        all_users = return_all_user(users)
        return all_users
    
    def get_user_logout(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        
        user = storage.find_by(User, **{"email":object_meta_data["email"]})
        print("user", user)
        if user is not None:
            login_history = storage.find_by(LoginHistory, **{"user_id":user.id})
            return {"user": user.to_dict(), "login_history":login_history.to_dict()}
        else:
            return None
            

def _hash_password(password: str) -> bytes:
    """ Hash password
    """
    return hashpw(password.encode(), gensalt())



def valid_login(user, password: str) -> bool:
    """ Login validation
    """
    try:
        hashed_password = user.hashed_password
        return checkpw(password.encode(),
            hashed_password.encode('utf-8'))
    except (NoResultFound, InvalidRequestError):
        return False
        
def return_all_user(users:List[User]):
    if users is not None:
        all_element:List[Dict[str, Any]] = []
        for element in users:
            user_data:UserEntity = UserEntity(element)
            all_element.append(user_data.to_dict())
        return all_element
    else:
        return []
