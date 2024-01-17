from typing import Dict, TypeVar
from models import storage
from models.booking import Booking, BookingStatus
from models.invoice import Invoice, InvoiceStatus
from models.room import Room, RoomStatus
from models.room_occupation import RoomOccupation
from models.settlement import Settlement
from models.settlement_invoice import SettlementInvoice
from services.occupation.occupation_adapter import return_all_room_items
from services.occupation.occupation_util import InvoiceNumberGenerator, InvoiceNumberGeneratorInterface, ObjectManager, ObjectManagerInvoice, RandomPartStrategy, reformat_request_data, reformat_request_datas
from models.room_category import RoomCategory
T = TypeVar('T')
class BookingService():
    def all_available_room(self, **kwargs):
        """AI is creating summary for all_available_room

        Returns:
            [type]: [description]
        """
        all_room_occupied = storage.get_room_with_date_interval(RoomOccupation, kwargs["start_date"], kwargs["end_date"])
        all_room_reserved_and_confirmed = storage.get_object_by_date_interval_and_filters(Booking, kwargs["start_date"], kwargs["start_date"], **{"is_deleted": False, "booking_status":BookingStatus.CONFIRMED.value})
        all_room_reserved = storage.get_object_by_date_interval_and_filters(Booking, kwargs["start_date"], kwargs["end_date"], **{"is_deleted": False, "booking_status":BookingStatus.PENDING.value})
        all_room_reserved_progress = storage.get_object_by_date_interval_and_filters(Booking, kwargs["start_date"], kwargs["end_date"], **{"is_deleted": False, "booking_status":BookingStatus.PROGRESS.value})
        
        
        
        all_room_reserved.extend(all_room_reserved_and_confirmed) if all_room_reserved is not None else [] 
        all_room_reserved.extend(all_room_reserved_progress) if all_room_reserved is not None else []
        all_rooms = storage.find_all_by(Room, **{"is_deleted": False})
        
        all_reserved_room_ids = [room.room_id for room in all_room_reserved]
        occupied_room_ids = [room.room_id for room in all_room_occupied]
        all_room_ids = [room.id for room in all_rooms]
        
        available_rooms_ids = list(set(all_room_ids) - set(occupied_room_ids))
        
        print("availlable room", available_rooms_ids)
        
        all_room_reserved_ids = list(set(available_rooms_ids) - set(all_reserved_room_ids))
        
        available_rooms = [storage.find_by(Room, id=room_id) for room_id in all_room_reserved_ids]
        
        #print("availlable_chambre", available_rooms)
        
        all_room_data = return_all_room_items(available_rooms)
        return all_room_data
    
    
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
        invoice_generator = InvoiceNumberGenerator(strategy=random_strategy)
        invoice_number = invoice_generator.generate_invoice_number()
        object_meta_data["invoice_number"] = invoice_number
        object_meta_data["invoice_amount"] = 0
        object_meta_data["invoice_status"] = InvoiceStatus.UNPAID.value
        object_meta_data["booking_status"] = BookingStatus.PENDING.value
        
        data = reformat_request_data(object_meta_data)
        invoice:Invoice = ObjectManager(data).create_invoice()
        data = reformat_request_data(object_meta_data)
        booking: Booking = ObjectManager(data).create_booking()

        try:
            all_object = {}
            booking.save()
            invoice.save()
            storage.update_object(Room,room.id, **{"room_status":RoomStatus.RESERVED.value})
            all_object["invoice"] = invoice.to_dict()
            all_object["reservation"] = booking.to_dict()
            return all_object
        except Exception as e:
            print(e)
            return None
        
    
    def confirmed_booking(
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
        booking = storage.find_by(Booking, id = object_meta_data["booking_id"])
        invoice = storage.find_by(Invoice, id = object_meta_data["invoice_id"])
        room = storage.find_by(Room, id = booking.room_id)
        price = object_meta_data["percentage"] * room.room_amount // 100
        object_meta_data["settlement_amount"] = price
        settlement:Settlement = ObjectManagerInvoice(data).create_settelement()
        object_meta_data["settlement_id"]= settlement.id
        data = reformat_request_datas(object_meta_data)
        settlemen_invoice:SettlementInvoice = ObjectManagerInvoice(data).create_settlement_invoice()
        
        try:
            storage.update_object(Room,room.id, **{"room_status":RoomStatus.RESERVED_AND_CONFIRMED.value})
            storage.update_object(Invoice,invoice.id, **{"invoice_status":InvoiceStatus.PAID.value, "invoice_amount":price})
            storage.update_object(Booking,booking.id, **{"booking_status":BookingStatus.CONFIRMED.value, "percentage":object_meta_data["booking_id"], "booking_price":price})
            settlement.save()
            settlemen_invoice.save()
        except Exception as e:
            print(e)
            return None
        

    def list_booking(self):
        all_booking_room = []
        bookings = storage.find_all_by(Booking, **{"is_deleted": False, "booking_status":BookingStatus.PENDING.value})
        
        for booking in bookings:
            room = storage.find_by(Room, **{"is_deleted": False, "id":booking.room_id, "room_status":RoomStatus.RESERVED.value})
            room_category = storage.find_by(RoomCategory, **{"is_deleted": False, "id":room.room_category_id})
            room_booked = {"booking":booking.to_dict(), "room":room.to_dict(), "room_category":room_category.to_dict()}
            all_booking_room.append(room_booked)
        return all_booking_room