from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional
from domain.client.email_value_object import EmailAddress
from domain.client.phone_value_object import PhoneNumber
from models.customer_type import CustormerType
from domain.client.date_value_object import DateValue
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from models.customer import Customer


@dataclass
class ClientData:
    id:str
    customer: Customer
    __date :DateValue =  Optional[DateValue]
    type_customer: CustormerType = Optional[CustormerType]
    __telephone: PhoneNumber = Optional[PhoneNumber]
    __email: EmailAddress = Optional[EmailAddress]
    def __post_init__(self):
        self.type_customer = self.get_client_type_by_id()
        self.__date = self.get_date()
        self.__email = self.get_email()
        self.__telephone = self.get_phone_number()
    
    def get_date(self)-> datetime:
        date: DateValue = DateValue(self.customer.date_of_birth) if self.customer.date_of_birth is not None else datetime.utcnow()
        return date
      
    def get_email(self):
        email: EmailAddress = EmailAddress(self.customer.email)
        return email
    
    def get_phone_number(self):
        phone_number: PhoneNumber = PhoneNumber(self.customer.phone_number)
        return phone_number
        
    
    def get_client_type_by_id(self)->CustormerType:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        ids = self.customer
        customer_type = obj.find_object_by(CustormerType, **{"id":ids.customer_type_id})
        return customer_type
    
    
    def map_customer_entity_to_customer_orm(self)-> Customer:
        customer_orm: Customer = Customer(
        id = self.id,
        user_id = self.user_id,
        last_name = self.customer.last_name,
        first_name = self.customer.first_name,
        gender = self.customer.gender,
        phone_number = self.telephone.phone_number,
        date_of_birth = self.date.date,
        email = self.email.email,
        institute_name = self.customer.institute_name,
        customer_type_id = self.type_customer.id)
        return customer_orm

        
    def map_customer_orm_to_customer_entity(self)-> "ClientData":
        customer_entity = ClientData(
        id = self.customer.id,
        type_customer = self.type_customer
        )
        return customer_entity
    
    @property
    def date(self):
        return self.__date
    
    @property
    def telephone(self):
        return self.__telephone
    
    @property
    def email(self):
        return self.__email

        
    def to_dict(self):
        """creates dictionary of the class and returns
        Return:
        returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        keys_to_convert = {"type_customer","customer"}
        
        for element in keys_to_convert:
            if element in my_dict and my_dict[element] is not None:
                my_dict[element] = my_dict[element].to_dict()
        return my_dict


