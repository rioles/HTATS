from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from models.customer_type import CustormerType
from domain.client.client_entity import DateValue
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from models.customer import Customer


@dataclass
class ClientData:
    id:str
    customer: Customer
    __date : Optional[datetime]
    type_customer: Optional[CustormerType]
    def __post_init__(self):
        self.type_customer = self.get_client_type_by_id()
        self.__date = self.get_date()
    
    def get_date(self)-> datetime:
        date: datetime = DateValue(self.customer.date_of_birth)
        return date   
        
    def get_client_type_by_id(self)->CustormerType:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        customer_type = obj.find_object_by(CustormerType, **{"id":self.customer.customer_type_id})
        return customer_type
    
    
    def map_customer_entity_to_customer_orm(self)-> Customer:
        customer_orm: Customer = Customer(
        id = self.id,
        last_name = self.customer.last_name,
        first_name = self.customer.first_name,
        gender = self.customer.gender,
        phone_number = self.customer.phone_number,
        date_of_birth = self.__date.date,
        sexe = self.customer.sexe,
        customer_type_id = self.type_customer.id)
        return customer_orm

        
    def map_customer_orm_to_customer_entity(self)-> "ClientData":
        customer_entity = ClientData(
        id = self.customer.id,
        type_customer = self.type_customer,
        __date = self.get_date() )
        return customer_entity

  