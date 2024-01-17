from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from models.settlement import Settlement
from typing import Any, Dict, List, Optional
from domain.client.client_entity import ClientData
from models.user import User
from models.customer import Customer
from models.invoice import Invoice
from models import storage
from models.settlement_invoice import SettlementInvoice
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface

@dataclass
class SettlementUser:
    user: User
    meta_data:Dict[str,Any]
    is_user_includ:bool =  True
    amount:Decimal = 0.00
    settlements: List[Settlement] = field(default_factory=list)
    customers:List[Dict[str, Any]] = field(default_factory=list)
    
    
    
    def __post_init__(self):
        self.settlements = self.get_settlements_object_by_users()
        self.customers = self.get_customers_data()
        self.amount = self.get_sum()
        
        
    def get_settlement_by_user(self):
        print("just to see",self.user)
        settlemens = storage.find_all_by(Settlement, **{"user_id": self.user.id})
        return settlemens
    
    def get_settlements_object_by_user(self) -> List[Settlement]:
        if self.is_user_includ == True:
            settlements = storage.get_object_by_date_interval_and_filter(Settlement, self.meta_data["start_date"], self.meta_data["end_date"], **{"user_id": self.user.id, "is_deleted":False} )
            return settlements
        else:
            settlements = storage.get_object_by_date_interval_and_filter(Settlement, self.meta_data["start_date"], self.meta_data["end_date"], **{"is_deleted":False} )

        return settlements
    
    def get_settlements_object_by_users(self) -> List[Settlement]:
        settlement_objects = []
        settlements = self.get_settlements_object_by_user()
        for settlement in settlements:
            settlement_objects.append(settlement.to_dict())
            
        return settlement_objects
    
    def get_settlemen_invoice(self) -> List[SettlementInvoice]:
        settlements = self.get_settlement_by_user()
        settlement_invoices = []
        for settlement in settlements:
            obj: ObjectManagerInterface = ObjectManagerAdapter()
            settlement_invoice = obj.find_object_by(SettlementInvoice, **{"settlement_id":settlement.id, "user_id":self.user.id})
            settlement_invoices.append(settlement_invoice)
        return settlement_invoices
    
    def get_invoices(self)-> List[Invoice]:
        settlement_invoices: List[SettlementInvoice] = self.get_settlemen_invoice()
        invoices = []
        for settlement_invoice in settlement_invoices:
            obj: ObjectManagerInterface = ObjectManagerAdapter()
            invoice = obj.find_object_by(Invoice, **{"id":settlement_invoice.invoice_id, "user_id":self.user.id})
            invoices.append(invoice)
        return invoices
    
    def get_customers(self) -> List[Customer]:
        invoices:List[Invoice] = self.get_invoices()
        customers = []
        for invoice in invoices:
            obj: ObjectManagerInterface = ObjectManagerAdapter()
            customer = obj.find_object_by(Customer, **{"id":invoice.customer_id, "user_id":self.user.id})
            customers.append(customer)
        return customers
    
    def get_customers_data(self) -> List[Dict[str,Any]]:
        customers:List[Customer] = self.get_customers()
        client_datas:List[Dict[str, Any]] = []
        for customer in customers:
            if customer is not None:
                client_data:ClientData = ClientData(customer.id, customer)
            client_datas.append(client_data.to_dict())
        return client_datas
    
    def get_sum(self) -> Decimal:
        total_amount = storage.get_sum_with_filter_and_interval(Settlement, self.meta_data["start_date"], self.meta_data["end_date"], "settlement_amount", **{"user_id":self.user.id})
        return total_amount
    
    
    
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        print(my_dict)
        keys = {"settlements","customers","amount"}

        
        for key in my_dict:
            if key in keys and key is not None:
                my_dict[key] = my_dict[key]
            else:
                if key == "meta_data" or key == "is_user_includ":
                    continue
                my_dict[key] = my_dict[key].to_dict()
                
        return my_dict
            
            
        