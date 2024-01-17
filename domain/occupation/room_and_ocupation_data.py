from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional
from domain.client.email_value_object import EmailAddress
from domain.client.phone_value_object import PhoneNumber
from models.booking import Booking
from models.customer_type import CustormerType
from domain.client.date_value_object import DateValue
from models.room_occupants import RoomOccupants
from services.object_manager_adapter import ObjectManagerAdapter
from services.object_manager_interface import ObjectManagerInterface
from models.customer import Customer
from models.invoice import Invoice, InvoiceStatus
from models.room_occupation import RoomOccupation
from models.room import Room
from models import storage
from services.occupation.occupation_util import calculate_number_of_nights
@dataclass
class RoomOccupationEntityData:
    status: str
    room: Room
    number_of_day:int = Optional[int]
    customer: Customer = Optional[Customer]
    room_occupation:RoomOccupation = Optional[RoomOccupation]
    room_occupants:List[RoomOccupants] = field(default_factory=list)

    
    def __post_init__(self):
        self.room_occupants = self.get_room_occupants_by_room_occupation()
        self.room_occupation = self.get_room_occupation_by_room()
        self.number_of_day = self.num_of_day()
        self.customer = self.client_provider()

    
    def get_room_occupation_by_room(self)->RoomOccupation:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        ids = self.room
        room_occupation = obj.find_object_by(RoomOccupation, **{"room_id":ids.id, "is_deleted":False})
        return room_occupation
    
    def get_client_by_booking(self):
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        ids = self.room
        booked_room = obj.find_object_by(Booking, **{"room_id":ids.id, "is_deleted":False})
        invoice = obj.find_object_by(Invoice, **{"id":booked_room.invoice_id, "is_deleted":False})
        customer_id = invoice.customer_id if invoice is not None else None
        customer = obj.find_object_by(Customer, **{"id":customer_id}) if customer_id is not None else None
        return customer
        
    
    def get_client_by_room_occupation(self)->List[Invoice]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        occupation = self.get_room_occupation_by_room()
        invoice = obj.find_object_by(Invoice, **{"id":occupation.invoice_id}) if occupation is not None else None
        customer_id = invoice.customer_id if invoice is not None else None
        customer = obj.find_object_by(Customer, **{"id":customer_id}) if customer_id is not None else None      
        return customer
    
    def client_provider(self):
        if self.status == "Reserved":
            return self.get_client_by_booking()
        else:
            return self.get_client_by_room_occupation()
        
        
    
    def num_of_day(self):
        occupation = self.get_room_occupation_by_room()
        return calculate_number_of_nights(occupation.start_date, occupation.end_date) if occupation is not None else None
    
    def get_room_occupants_by_room_occupation(self)->List[Invoice]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        occupation = self.get_room_occupation_by_room()
        occupants = obj.find_all_with_filter(RoomOccupants, **{"occupation_id":occupation.id}) if occupation is not None else None       
        return occupants
    
    
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        print(my_dict)
        keys = {"customer", "room","room_occupation"}

        for key in my_dict:
            if key is not None and  key in keys and my_dict[key] is not None:
                my_dict[key] = my_dict[key].to_dict()
            else:
                my_dict[key] = my_dict[key]
        return my_dict
    

@dataclass
class RoomOccupationData:
    room_occupant:RoomOccupants
    room_occupation:RoomOccupation = Optional[RoomOccupation]
    room: Room = Optional[Room]
    
    def __post_init__(self):
        self.room_occupation = self.get_room_occupation_by_room_occupant()
        self.room = self.get_room_by_room_occupation()
        
    def get_room_occupation_by_room_occupant(self):
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        occupation = obj.find_object_by(RoomOccupation, **{"id":self.room_occupant.occupation_id}) 
        return occupation
    
    def get_room_by_room_occupation(self):
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        occupation = self.get_room_occupation_by_room_occupant()
        room = obj.find_object_by(RoomOccupation, **{"id":occupation.room_id}) 
        return room
    
    def to_dict(self):
        """creates dictionary of the class  and returns
        Return:
            returns a dictionary of all the key values in __dict__
        """
        my_dict = dict(self.__dict__)
        print(my_dict)
        keys = {"room_occupant", "room","room_occupation"}

        for key in my_dict:
            if key is not None and  key in keys and my_dict[key] is not None:
                my_dict[key] = my_dict[key].to_dict()
            else:
                my_dict[key] = my_dict[key]
        return my_dict

        
