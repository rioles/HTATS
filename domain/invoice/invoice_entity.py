from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional
from domain.client.email_value_object import EmailAddress
from domain.client.phone_value_object import PhoneNumber
from models.customer_type import CustormerType
from domain.client.date_value_object import DateValue
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from models.customer import Customer
from models.invoice import Invoice, InvoiceStatus
from models.room_occupation import RoomOccupation
from models.room import Room
from models import storage
from services.occupation.occupation_util import calculate_number_of_nights


@dataclass
class InvoiceEntity:
    customer: Customer
    meta_data:Dict[str,Any]
    include_paid: bool = False
    invoice_amount:Decimal = 0.00
    invoice:Invoice = field(default_factory=list)
    customer_type:CustormerType = Optional[CustormerType]

    
    def __post_init__(self):
        self.invoice_amount = self.get_unpaid_incoice_amout()
        self.invoice = self.get_invoice_object()
        self.customer_type = self.get_client_type_by_id()
        

    def get_unpaid_incoice_amout(self) -> Decimal:
        if self.include_paid == False:
            total_amount = storage.get_sum_with_filter_and_interval(Invoice, self.meta_data["start_date"], self.meta_data["end_date"], "invoice_amount", **{"invoice_status":InvoiceStatus.UNPAID.value,"customer_id":self.customer.id})
            print("rrrrr", total_amount)
            return total_amount
        else:
           return storage.get_sum_with_filter_and_interval(Invoice, self.meta_data["start_date"], self.meta_data["end_date"], "invoice_amount", **{"customer_id":self.customer.id,"is_deleted":False})
  
    def get_invoice_object_by_cust(self) -> List[Invoice]:
        if self.include_paid == False:
            invoices = storage.get_object_by_date_interval_and_filter(Invoice, self.meta_data["start_date"], self.meta_data["end_date"], **{"invoice_status":InvoiceStatus.UNPAID.value, "is_deleted":False, "customer_id":self.customer.id} )
            return invoices
        else:
            invoices = storage.get_object_by_date_interval_and_filter(Invoice, self.meta_data["start_date"], self.meta_data["end_date"], **{"is_deleted":False, "customer_id":self.customer.id} ) 
        return invoices
    
    def get_invoice_object(self) -> List[Dict[str, Any]]:
        invoice_objects = []
        invoices = self.get_invoice_object_by_cust()
        for invoice in invoices:
            invoice_objects.append(invoice.to_dict())
            
        return invoice_objects
    
    def get_customers(self) -> List[Customer]:
        invoices:List[Invoice] = self.get_invoice_object_by_cust()
        customers = []
        for invoice in invoices:
            obj: ObjectManagerInterface = ObjectManagerAdapter()
            customer = obj.find_object_by(Customer, **{"id":invoice.customer_id, "is_deleted":False})
            customers.append(customer)
        return customers
    
    def get_client_type_by_id(self)->CustormerType:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        ids = self.customer
        customer_type = obj.find_object_by(CustormerType, **{"id":ids.customer_type_id})
        return customer_type
    
    
    
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        print(my_dict)
        keys = {"customer","customer_type"}

        
        for key in my_dict:
            if key in keys and key is not None:
                my_dict[key] = my_dict[key].to_dict()
            else:
                my_dict[key] = my_dict[key]                
        return my_dict
            
            
        