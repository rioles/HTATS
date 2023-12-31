from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Dict, List, Optional, TypeVar, Union
from domain.occupation.invoice_customer import InvoiceData, RoomOccupationData
from domain.occupation.room_and_ocupation_data import RoomOccupationEntityData
from domain.room.room_entity import RoomDataAgregate
from models.invoice import InvoiceStatus, Invoice
from models.room_occupation import RoomOccupation
from models.room_occupants import RoomOccupants
from models.customer import Customer

from models.room import Room, RoomStatus
from models.settlement import Settlement
from models.settlement_invoice import SettlementInvoice
from services.occupation.occupation_port import OccupationPort
from services.occupation.occupation_util import InvoiceNumberGenerator, ObjectManager, RandomPartStrategy, reformat_request_data, reformat_request_datas,ObjectManagerInvoice, calculate_number_of_nights
T = TypeVar('T')  # Type variable for the current class
from models import storage
from models.customer import Customer

class OccupationAdapter(OccupationPort):
    def add_object(
        self,
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
        room = storage.find_by(Room, id = object_meta_data["room_id"])
        random_strategy = RandomPartStrategy()
        invoice_generator = InvoiceNumberGenerator(random_strategy)
        number_of_day = calculate_number_of_nights(object_meta_data["start_date"], object_meta_data["end_date"])
        invoice_number = invoice_generator.generate_invoice_number()
        object_meta_data["invoice_number"] = invoice_number
        object_meta_data["invoice_amount"] = room.room_amount * number_of_day
        object_meta_data["invoice_status"] = InvoiceStatus.UNPAID.value
        
        data = reformat_request_data(object_meta_data)
        invoice:Invoice = ObjectManager(data).create_invoice()
        print(invoice)
        object_meta_data["invoice_id"] = invoice.id
        data = reformat_request_data(object_meta_data)
        room_occupation: RoomOccupation = ObjectManager(data).create_occupation()
        object_meta_data["occupation_id"] = room_occupation.id
        data = reformat_request_data(object_meta_data)
        try:
            all_object = {}
            storage.update_object(Room,room.id, **{"room_status":RoomStatus.OCCUPIED.value})
            invoice.save()
            room_occupation.save()
            all_object["invoice"] = invoice.to_dict()
            all_object["room_occupation"] = room_occupation.to_dict()
            return all_object
        except Exception as e:
            print(e)
            return None
    
    
    def add_object_occupant(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        """
        Registers an object in the database.

        Args:
            object: A dictionary of properties of the user to register.

        Returns:
            The room_occupant object, if the room_occupant was registered successfully.

        Raises:
            Exception: If the user_object dictionary is empty.
    
    """
        data = reformat_request_data(object_meta_data)
        #occupation_id = storage.find_by(RoomOccupation, **{"id":object_meta_data["occupation_id"]})
        #object_meta_data["occupation_id"] = occupation_id
        data = reformat_request_data(object_meta_data)
        print(object_meta_data)
        room_occupant:RoomOccupants = ObjectManager(data).create_occupant()
        print("occupant_object",room_occupant)
        try:
            room_occupant.save()
            return room_occupant.to_dict()
        except Exception as e:
            print(e)
            return None
    
       
        
    def find_object_by_intervall(
        self,
        object_class: T,
        start_date: Union[str, datetime],
        end_date: Union[str, datetime],
        room_class: Room
    ) -> T:

        """
        Finds an object in the storage.

        Args:
            object_class: The class of the user to find.
            user_object: A criteria on which relies the object search.

        Returns:
            The  object, if found.
        """
        all_room_occupied = storage.get_room_with_date_interval(object_class, start_date, end_date)
        all_rooms = storage.find_all_by(Room, **{"room_status":RoomStatus.AVAILABLE_AND_CLEAN.value})
        occupied_room_ids = [room.room_id for room in all_room_occupied]
        all_room_ids = [room.id for room in all_rooms]
        
        available_rooms_ids = list(set(all_room_ids) - set(occupied_room_ids))
        available_rooms = [storage.find_by(Room, id=room_id) for room_id in available_rooms_ids]
        
        all_room_data = return_all_room_items(available_rooms)
        return all_room_data
    
    def find_all_ivoice_by_customer(
        self
    ) -> T:
        object_filter = {"invoice_status":InvoiceStatus.UNPAID.value}
        customers = storage.find_all_with_join(Customer, Invoice, **object_filter)
        print("my_type",type(customers[0]))
        all_invoice = all_invoice_by_client(customers)
        return all_invoice
    
    def find_all_both_ivoice_by_customer(
        self
    ) -> T:
        
        customers = storage.find_all_with_joins(Customer, Invoice)
        print("my_type",type(customers[0]))
        all_invoice = all_invoice_by_customer(customers)
        return all_invoice
        
        
    def make_payment(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        invoice = storage.find_by(Invoice, **{"id":object_meta_data["invoice_id"]})
        storage.update_object(Invoice,invoice.id, **{"invoice_status":InvoiceStatus.PAID.value})
        object_meta_data["settlement_amount"]= invoice.invoice_amount
        data = reformat_request_datas(object_meta_data)
        settlement:Settlement = ObjectManagerInvoice(data).create_settelement()
        object_meta_data["settlement_id"]= settlement.id
        data = reformat_request_datas(object_meta_data)
        settlemen_invoice:SettlementInvoice = ObjectManagerInvoice(data).create_settlement_invoice()
        settlement.save()
        settlemen_invoice.save()
        invoice = storage.find_by(Invoice, **{"id":object_meta_data["invoice_id"]})
        return {"settlement":settlement.to_dict(), "settlemen_invoice":settlemen_invoice.to_dict(), "invoice":invoice.to_dict()}

    def get_occupation_and_room_by_invoice(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        """
        """
        invoice =  storage.find_by(Invoice, **{"id":object_meta_data["invoice_id"]})
        room_occupation_adapter = RoomOccupationData(invoice)
        return room_occupation_adapter.to_dict()
    
    def update_room_status(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        """
        """
        
    def get_room_entity_data(
        self,
        **object_meta_data: Dict[str, str]
    ) -> T:
        """
        """
        room = storage.find_by(Room, **{"id":object_meta_data["id"]})
        room_entity_data:RoomOccupationEntityData = RoomOccupationEntityData(room)
        return room_entity_data.to_dict()
    
    def vacate_room(
        self, 
        **object_meta_data: Dict[str, str]
    ) -> Room:
        """
            Free up a room by deleting the room occupation and updating the room 
            status to new status.

        Parameters:
        - object_meta_data (Dict[str, str]): Metadata associated with the room to be vacated and room_occupation.
        Returns:
        - T: The room updated. 
        """
        room_occupation = storage.find_by(RoomOccupation, **{"id":object_meta_data["room_occupation_id"]})
        storage.update_object(Room,object_meta_data["room_id"], **{"room_status":object_meta_data["room_status"]})
        room_occupation.delete()
        room = storage.find_by(Room, **{"id":object_meta_data["room_id"]})
        return room.to_dict()
    
#RoomOccupationEntityData
def return_all_room_items(rooms:List[Room]):
    if rooms is not None:
        all_element:List[Dict[str, Any]] = []
        for element in rooms:
            room_data:RoomDataAgregate = RoomDataAgregate(element)
            all_element.append(room_data.to_dict())
        return all_element
    else:
        return []
    
def all_invoice_by_client(customers:List[Customer]):
    if customers is not None:
        all_element:List[Dict[str, Any]] = []
        for element in customers:
            invoice_data:InvoiceData = InvoiceData(element)
            all_element.append(invoice_data.to_dict())
        return all_element
    else:
        return []
    
def all_invoice_by_customer(customers:List[Customer]):
    include_paid = True
    if customers is not None:
        all_element:List[Dict[str, Any]] = []
        for element in customers:
            invoice_data:InvoiceData = InvoiceData(element, include_paid)
            all_element.append(invoice_data.to_dict())
        return all_element
    else:
        return []


#filter = {"invoice_status":InvoiceStatus.UNPAID.value}
#ivoice = storage.find_all_with_join(Customer, Invoice, **filter)
#print(ivoice[0].to_dict())
date_string = "2023-11-28T15:30:00"
f_date = "2023-11-29T13:32:44"
datetime_object = datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S")
datetime_object2 = datetime.strptime(f_date, "%Y-%m-%dT%H:%M:%S")
all_room_occupied = storage.get_room_with_date_interval(RoomOccupation, datetime_object, datetime_object2)
print(all_room_occupied)
invoice = storage.find_by(Invoice, **{"id":""})
#storage.update_object(Invoice,invoice.id, **{"invoice_status":InvoiceStatus.UNPAID.value})
#a =  InvoiceData(ivoice[0])
print(invoice)
#print("aalal",a.get_invoice_by_customer())
#print("dict",a.to_dict())