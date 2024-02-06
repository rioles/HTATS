from dataclasses import dataclass, field
from decimal import Decimal
from typing import Dict, List, Optional
from models.booking import Booking
from models.customer_type import CustormerType
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from models.customer import Customer
from models.invoice import Invoice, InvoiceStatus
from models.room_occupation import RoomOccupation
from models.room import Room
from models import storage
from services.occupation.occupation_util import calculate_number_of_nights


@dataclass
class InvoiceData:
    customer: Customer
    include_paid: bool = False
    invoice:Invoice = field(default_factory=list)
    customer_type:CustormerType = Optional[CustormerType]
    amount:Decimal = 0.00
    
    def __post_init__(self):
        self.invoice = self.get_invoice_by_customer()
        self.customer_type = self.get_client_type_by_id()
        self.amount = self.get_total_amount()
    
    def get_client_type_by_id(self)->CustormerType:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        ids = self.customer
        customer_type = obj.find_object_by(CustormerType, **{"id":ids.customer_type_id})
        return customer_type
    
    
    def get_invoice_by_customer(self)->List[Invoice]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        if self.include_paid == False:
            invoices = obj.find_all_posi_with_filter(Invoice, **{"customer_id":self.customer.id, "invoice_status":InvoiceStatus.UNPAID.value, "is_deleted":False})
            return invoices
        else:
            invoices = obj.find_all_posi_with_filter(Invoice, **{"customer_id":self.customer.id, "is_deleted":False})
            
            return invoices
    
    def get_total_amount(self)->Decimal:
        sum_amount = storage.get_sum_with_filter(Invoice, "invoice_amount", **{"invoice_status":InvoiceStatus.UNPAID.value, "customer_id":self.customer.id})
        return sum_amount
    
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        print(my_dict)
        keys = {"customer", "room_orm","customer_type"}

        
        for key in my_dict:
            if key in keys and key is not None:
                my_dict[key] = my_dict[key].to_dict()
            else:
                my_dict[key] = my_dict[key]
        return my_dict


@dataclass
class RoomOccupationData:
    invoice: Invoice
    number_of_day:int = Optional[int]
    room: Room = Optional[Room]
    room_occupation:RoomOccupation = Optional[RoomOccupation]
    booking:Booking = Optional[Booking]

    
    def __post_init__(self):
        self.room = self.get_room_by_room_occupation()
        self.room_occupation = self.get_room_occupation_by_invoice()
        self.number_of_day = self.num_of_day()
        self.booking = self.get_booking_by_invoice()

    
    def get_room_occupation_by_invoice(self)->RoomOccupation:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        ids = self.invoice
        room_occupation = obj.find_object_by(RoomOccupation, **{"invoice_id":ids.id})
        return room_occupation
    
    def get_booking_by_invoice(self):
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        ids = self.invoice
        booking = obj.find_object_by(Booking, **{"invoice_id":ids.id})
        return booking
        
    
    def get_room_by_room_occupation(self)->List[Invoice]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        occupation = self.get_room_occupation_by_invoice()
        booking = self.get_booking_by_invoice()
        
        if occupation is not None:
            return obj.find_object_by(Room, **{"id":occupation.room_id})
        else:
            return obj.find_object_by(Room, **{"id":booking.room_id})      
    
    def num_of_day(self):
        occupation = self.get_room_occupation_by_invoice()
        if occupation is not None:
            return calculate_number_of_nights(occupation.start_date, occupation.end_date)
        return 0
    
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        print(my_dict)
        keys = {"invoice", "room","room_occupation","booking"}

        for key in my_dict:
            if key in keys:
                if my_dict[key] is not None:
                    my_dict[key] = my_dict[key].to_dict()
            else:
                my_dict[key] = my_dict[key]
        return my_dict
               
        
 


    