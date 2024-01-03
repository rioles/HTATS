from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional
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

