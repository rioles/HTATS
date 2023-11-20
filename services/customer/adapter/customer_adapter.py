from typing import Any, Dict, List, Optional, TypeVar
from domain.client.client_entity import ClientData
from models.customer import Customer
from services.customer.port.customer_port import CustormPort
from services.object_manager_interface import ObjectManagerInterface
from services.object_manager_adapter import ObjectManagerAdapter
from models import storage

T = TypeVar('T')

class CustomerAdapter(CustormPort):
    def add_object(self,
                 current_class: Customer,
                 **object_meta_data: Dict[str, Any]
                 ) -> Optional[T]:
        client_entity:ClientData = Optional[ClientData]
        try:
            customer:Customer = Customer(**object_meta_data)
            if get_customer_by_phone(customer) is not None:
                return get_customer_by_phone(customer)
            else:
                client_entity:ClientData = ClientData(customer.id, customer)
                customer_from_entity:Customer = client_entity.map_customer_entity_to_customer_orm()
                customer_from_entity.save()

            
        except Exception as e:
            print(e)
            return None
        return client_entity.to_dict()
    
 
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
        return storage.get_all(current_class)

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
        all_customer: List[Customer] = self.find_all_object(customer_object)
        all_element:List[Dict[str, Any]] = []
        
        
        for element in all_customer:
            client_data:ClientData = ClientData(element.id, element)
            all_element.append(client_data.to_dict())
        return all_element
    
    
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
        if object_find is not None:
            client_data:ClientData = ClientData(object_find.id, object_find)
            return client_data.to_dict()
        return None
    
        
    
def get_customer_by_phone(objs: Customer):
    obj: ObjectManagerInterface = ObjectManagerAdapter()
    cust = obj.find_object_by(Customer, **{"phone_number":objs.phone_number})
    return cust

a:CustomerAdapter = CustomerAdapter()
print(a.find_object_by(Customer, **{"phone_number": "96363651"}))