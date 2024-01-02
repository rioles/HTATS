    
from typing import  Dict
from models.invoice import Invoice
from models.room_occupants import RoomOccupants
from models.room_occupation import RoomOccupation
from services.room_service.room.adapter.room_item_adapter import return_element
from models.settlement import Settlement
from models.settlement_invoice import SettlementInvoice
import random
import string
from abc import ABC, abstractmethod
from datetime import datetime, time
from dateutil import parser

def reformat_request_data(request_data: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    """
    Reformat and preprocess the provided request data to transform it from an initial format
    to a desired format where occupation-related, invoice-related, and occupant-related data
    are organized within respective sub-dictionaries.

    This abstract method allows subclasses to implement custom logic for reformatting and
    organizing the input request data. It is typically used when the incoming data structure
    requires segmentation into specific categories, such as occupation-related, invoice-related,
    and occupant-related data.

    Parameters:
        request_data (Dict[str, str]): The input request data in its initial format.

    Returns:
        Dict[str, Dict[str, str]]: The reformatted request data in the desired format, where
        occupation-related, invoice-related, and occupant-related data are organized within
        respective sub-dictionaries.
    """
    request_data_reformat = {}
    
    # Keys for occupation-related data
    occupation_key = {"user_id","room_id", "start_date", "end_date", "invoice_id"}
    
    # Keys for invoice-related data
    invoice_key = {"user_id","invoice_number", "invoice_amount", "invoice_status", "customer_id"}
    
    # Keys for occupant-related data
    occupant_key = {"user_id","first_name", "last_name", "occupation_id", "gender", "phone_number",
                    "date_of_birth", "email", "document_number", "type_of_document", "institute_name"}
    
    # Extracting data for each category
    occupation_data = return_element(occupation_key, request_data)
    invoice_data = return_element(invoice_key, request_data)
    occupant_data = return_element(occupant_key, request_data)
   
    # Organizing data within respective sub-dictionaries
    request_data_reformat["occupation_data"] = occupation_data
    request_data_reformat["invoice_data"] = invoice_data
    request_data_reformat["occupant_data"] = occupant_data
    
    return request_data_reformat



class ObjectManager:
    def __init__(self, request_data: Dict):
        self.request_data = request_data

    def create_invoice(self):
        invoice_data = self.request_data["invoice_data"]
        return Invoice(**invoice_data)

    def create_occupation(self):
        occupation_data = self.request_data["occupation_data"]
        return RoomOccupation(**occupation_data)
    
    def create_occupant(self):
        occupant_data = self.request_data["occupant_data"]
        return RoomOccupants(**occupant_data)



class InvoiceNumberGeneratorInterface(ABC):
    @abstractmethod
    def generate(self, length):
        pass

class RandomPartStrategy(InvoiceNumberGeneratorInterface):
    def generate(self, length):
        random_part = ''.join(random.choices(string.digits + string.ascii_uppercase, k=length))
        return random_part

class InvoiceNumberGenerator:
    def __init__(self, strategy: InvoiceNumberGeneratorInterface):
        self.strategy = strategy

    def generate_invoice_number(self, length=10):
        return self.strategy.generate(length)



def reformat_request_datas(request_data: Dict[str, str]) -> Dict[str, Dict[str, str]]:
    """
    Reformat and preprocess the provided request data to transform it from an initial format
    to a desired format where occupation-related, invoice-related, and occupant-related data
    are organized within respective sub-dictionaries.

    This abstract method allows subclasses to implement custom logic for reformatting and
    organizing the input request data. It is typically used when the incoming data structure
    requires segmentation into specific categories, such as occupation-related, invoice-related,
    and occupant-related data.

    Parameters:
        request_data (Dict[str, str]): The input request data in its initial format.

    Returns:
        Dict[str, Dict[str, str]]: The reformatted request data in the desired format, where
        occupation-related, invoice-related, and occupant-related data are organized within
        respective sub-dictionaries.
    """
    request_data_reformat = {}
    
    # Keys for occupation-related data
    settlement_key = {"settlement_amount", "payment_type_id", "payer_phone"}
    
    # Keys for invoice-related data
    settlement_invoice_key = {"invoice_id", "settlement_id"}
    
    # Keys for occupant-related data
    
    settlement_data = return_element(settlement_key, request_data)
    settlement_invoice_data = return_element(settlement_invoice_key, request_data)
    
   
    # Organizing data within respective sub-dictionaries
    request_data_reformat["settlement_data"] = settlement_data
    request_data_reformat["settlement_invoice_data"] = settlement_invoice_data
    
    return request_data_reformat  

class ObjectManagerInvoice:
    def __init__(self, request_data: Dict):
        self.request_data = request_data

    def create_settelement(self):
        settelement_data = self.request_data["settlement_data"]
        return Settlement(**settelement_data)

    def create_settlement_invoice(self):
        settlement_invoice_data = self.request_data["settlement_invoice_data"]
        return SettlementInvoice(**settlement_invoice_data)
    

    


def calculate_number_of_nights(checkin_datetime, checkout_datetime):
    """
    Calculate the number of nights between check-in and check-out datetimes.

    Parameters:
        checkin_datetime (str or datetime): Check-in datetime in the format 'YYYY-MM-DDTHH:MM:SS' or datetime object.
        checkout_datetime (str or datetime): Check-out datetime in the format 'YYYY-MM-DDTHH:MM:SS' or datetime object.

    Returns:
        int: Number of nights.
    """
    if isinstance(checkin_datetime, str):
        checkin_dt = parser.parse(checkin_datetime)
    else:
        checkin_dt = checkin_datetime

    if isinstance(checkout_datetime, str):
        checkout_dt = parser.parse(checkout_datetime)
    else:
        checkout_dt = checkout_datetime

    # Calculate the number of nights, considering hours
    num_nights = (checkout_dt - checkin_dt).days

    # If the check-in time is before 12:00 PM, add one night
    if checkin_dt.time() < time(12, 0, 0):
        num_nights += 1

    # If the check-out time is greater than or equal to 12:00 PM, add one day
    if checkout_dt.time() >= time(12, 0, 0):
        num_nights += 1

    return num_nights
