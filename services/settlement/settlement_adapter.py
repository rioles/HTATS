from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, TypeVar, Union
from domain.invoice.invoice_entity import InvoiceEntity
from domain.settlement.settlement_data import SettlementUser
from models import storage
from models.invoice import Invoice, InvoiceStatus
from models.settlement import Settlement
from models.user import User
from services.settlement.settlement_port import SettlementPort
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from models.customer import Customer
TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"


T = TypeVar('T')  # Type variable for the current class


class SettlementAdapter(SettlementPort):
    def get_sum_with_intervall(
        self,
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, str]:
        
        current_datetime = datetime.now()
        start_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        sum_amount = storage.get_sum_with_filter_and_interval(Settlement, start_day, current_datetime, "settlement_amount", **{"user_id":object_meta_data["user_id"]})
        return {"total_amount":sum_amount}

    def get_settlement_list_by_criteria(
        self, 
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        user = obj.find_object_by(User, **{"id":object_meta_data["user_id"], "is_deleted":False})
        object_meta_data = convert_date_update_data(object_meta_data)   
        list_settlement = SettlementUser(user, object_meta_data)
        return list_settlement.to_dict()
 

    def get_unpaid_invoice_list_by_criteria(
        self, 
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        customer = obj.find_object_by(Customer, **{"id":object_meta_data["customer_id"],"is_deleted":False})
        object_meta_data = convert_date_update_data(object_meta_data)
        invoices = InvoiceEntity(customer, object_meta_data)
        return invoices.to_dict()
    
    def get_all_invoice_list_by_criteria(
        self, 
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        customer = obj.find_object_by(Customer, **{"id":object_meta_data["customer_id"],"is_deleted":False})
        object_meta_data = convert_date_update_data(object_meta_data)
        invoices = InvoiceEntity(customer, object_meta_data, True)
        return invoices.to_dict()
    
    def get_all_settlement_list_by_criteria(
        self, 
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        user = obj.find_object_by(User, **{"id":object_meta_data["user_id"], "is_deleted":False})
        object_meta_data = convert_date_update_data(object_meta_data)
        list_settlement = SettlementUser(user, False, object_meta_data)
        return list_settlement.to_dict()
    


def convert_to_timestamp(date_str: str) -> Union[None, datetime]:
    try:
        return datetime.strptime(date_str, TIMESTAMP_FORMAT)
    except ValueError:
        return None
    
def convert_date_update_data(object_meta_data:Dict[str,Any]):
    print(object_meta_data["start_date"])
    if isinstance(object_meta_data["start_date"], str):
        object_meta_data["start_date"] = convert_to_timestamp(object_meta_data["start_date"])  
    if isinstance(object_meta_data["end_date"], str):
        object_meta_data["start_date"] = convert_to_timestamp(object_meta_data["end_date"])
    return object_meta_data