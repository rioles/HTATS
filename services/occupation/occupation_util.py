from typing import  Dict
from models.booking import Booking
from models.invoice import Invoice
from models.room_occupants import RoomOccupants
from models.room_occupation import RoomOccupation
from services.room_service.room.adapter.room_item_adapter import return_element
from models.settlement import Settlement
from models.settlement_invoice import SettlementInvoice
from models.room import Room
from models.employee import Employee
from models.role import Role
from models.user import User
from models.user_role import UserRoles
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
    booking_key = {"booking_status", "booking_price", "room_id", "start_date", "end_date", "invoice_id",
                   "user_id","created_at","updated_at","is_deleted"}
    employee_key = {"user_id","first_name","last_name","gender","date_of_birth","phone_number","address","email"
                    ,"institute_name","document_number","type_of_document","profession","reason","id","created_at","updated_at","is_deleted"}
    room_key = {"room_label","room_amount","room_status","room_category_id","user_id","id","created_at","updated_at","is_deleted"}
    
    role_key = {"id","created_at","updated_at","is_deleted","role_name"}
    
    user_key = {"id","created_at","updated_at","is_deleted","role_name","username","email"}
    user_role_key = {"id","created_at","updated_at","is_deleted","role_name","username","email","user_id","role_id"}
    # Extracting data for each category
    occupation_data = return_element(occupation_key, request_data)
    invoice_data = return_element(invoice_key, request_data)
    occupant_data = return_element(occupant_key, request_data)
    booking_data = return_element(booking_key, request_data)
    employee_data = return_element(employee_key, request_data)
    room_data = return_element(room_key, request_data)
    role_data = return_element(role_key, request_data)
    user_data = return_element(user_key, request_data)
    user_role_data = return_element(user_role_key, request_data)
    
   
    # Organizing data within respective sub-dictionaries
    request_data_reformat["occupation_data"] = occupation_data
    request_data_reformat["invoice_data"] = invoice_data
    request_data_reformat["occupant_data"] = occupant_data
    request_data_reformat["booking_data"] = booking_data
    request_data_reformat["employee_data"] = employee_data
    request_data_reformat["room_data"] = room_data
    request_data_reformat["role_data"] = role_data
    request_data_reformat["user_role_data"] = user_role_data
    request_data_reformat["user_data"] = user_data
    
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
    
    def create_booking(self):
        booking_data = self.request_data["booking_data"]
        return Booking(**booking_data)
    
    def create_employee(self):
        employee_data = self.request_data["employee_data"]
        return Employee(**employee_data)
    
    def create_room(self):
        room_data = self.request_data["room_data"]
        return Room(**room_data)
    
    def create_role(self):
        role_data = self.request_data["role_data"]
        return Role(**role_data)
    
    def create_user_data(self):
        user_data = self.request_data["user_data"]
        return User(**user_data)
    
    def create_user_role_data(self):
        user_role_data = self.request_data["user_role_data"]
        return UserRoles(**user_role_data)



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
    settlement_key = {"user_id","settlement_amount", "payment_type_id", "payer_phone"}
    
    # Keys for invoice-related data
    settlement_invoice_key = {"user_id", "invoice_id", "settlement_id"}
    
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
    

    


def calculate_number_of_nightss(checkin_datetime, checkout_datetime):
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

def calculate_number_of_nights(checkin_datetime, checkout_datetime):
    """
    Calculate the number of nights between check-in and check-out datetimes,
    considering nights within a 12-hour window around midnight.

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

    # Calculate the number of nights based on days difference
    num_nights = (checkout_dt.date() - checkin_dt.date()).days

    # Check for nights within the 12-hour window

    # Night on check-in if before noon
    if checkin_dt.time() < time(12, 0, 0):
        num_nights += 1

    # Night on check-out if after or equal to noon on the next day
    if checkout_dt.time() >= time(12, 0, 0) and checkout_dt.date() > checkin_dt.date():
        num_nights += 1

    return num_nights




