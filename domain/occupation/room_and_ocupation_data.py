from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional
from domain.client.email_value_object import EmailAddress
from domain.client.phone_value_object import PhoneNumber
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
    room: Room
    number_of_day:int = Optional[int]
    customer: Customer = Optional[Room]
    room_occupation:RoomOccupation = Optional[RoomOccupation]
    room_occupants:List[RoomOccupants] = field(default_factory=list)

    
    def __post_init__(self):
        self.room_occupants = self.get_room_occupants_by_room_occupation()
        self.room_occupation = self.get_room_occupation_by_room()
        self.number_of_day = self.num_of_day()
        self.customer = self.get_client_by_room_occupation()

    
    def get_room_occupation_by_room(self)->RoomOccupation:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        ids = self.room
        room_occupation = obj.find_object_by(RoomOccupation, **{"room_id":ids.id})
        return room_occupation
    
    
    def get_client_by_room_occupation(self)->List[Invoice]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        occupation = self.get_room_occupation_by_room()
        invoice = obj.find_object_by(Invoice, **{"id":occupation.invoice_id})
        customer_id = invoice.customer_id
        customer = obj.find_object_by(Customer, **{"id":customer_id})        
        return customer
    
    def num_of_day(self):
        occupation = self.get_room_occupation_by_room()
        return calculate_number_of_nights(occupation.start_date, occupation.end_date)
    
    def get_room_occupants_by_room_occupation(self)->List[Invoice]:
        obj: ObjectManagerInterface = ObjectManagerAdapter()
        occupation = self.get_room_occupation_by_room()
        occupants = obj.find_all_with_filter(RoomOccupants, **{"occupation_id":occupation.id})        
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
            if key in keys and key is not None:
                my_dict[key] = my_dict[key].to_dict()
            else:
                my_dict[key] = my_dict[key]
        return my_dict