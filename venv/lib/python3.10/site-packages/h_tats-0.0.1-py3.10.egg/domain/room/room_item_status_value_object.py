from dataclasses import dataclass, field
from typing import Dict, Optional
from models.room import RoomStatus
from models.room_item import RoomItemStatus
@dataclass
class RoomItemStatusValueObject:
    __status: str = Optional[RoomItemStatus]
    __status_expected: Dict[str, str] = field(default_factory=lambda: {"Working": True, "Not_working": True})

    def __post_init__(self):
        if  self.__status not in self.__status_expected:
            raise ValueError("RoomItemStatus must be Working or Not_working")
        else:
            self.__status = self.check_status(self.__status)
  
    def check_status(self, status: str):
        if status in self.__status_expected:
            return RoomItemStatus(status)
        else:
            raise ValueError("RoomItemStatus must be Working or Not_working")
            
    @property
    def status(self):
        return self.__status


@dataclass
class RoomStatusValueObject:
    __status: str = Optional[RoomItemStatus]
    __status_expected: Dict[str, str] = field(default_factory=lambda: {"Available_and_dirty": True, "Available_and_clean": True, "Occupied": True, "Out_of_order": True})
    def __post_init__(self):
        if  self.__status not in self.__status_expected:
            raise ValueError("RoomStatus must be Available_and_dirty , Occupied, Available_and_clean, Out_of_order")
        else:
            self.__status = self.check_status(self.__status)
  
    def check_status(self, status: str):
        if status in self.__status_expected:
            return RoomStatus(status)
        else:
            raise ValueError("RoomItemStatus must be Working or Not_working")
            
    @property
    def status(self):
        return self.__status


a = RoomItemStatusValueObject("Not_working")
print(a.status.value)
b = RoomStatusValueObject("Occupied")
print(b.status.value)