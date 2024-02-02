from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class DateValue:
    __date: Optional[datetime] = None
    TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __post_init__(self):
        self.__check_date()

    @property
    def date(self):
        return self.__date.strftime(self.TIMESTAMP_FORMAT) if self.__date is not None else None

    def __check_date(self):
        if self.__date is None:
            raise ValueError("Date should not be None")

        if isinstance(self.__date, str):
            self._handle_string_date()

        elif isinstance(self.__date, datetime):
            self._handle_datetime_date()

        elif isinstance(self.__date, date):
            self._handle_date_date()
       
    def _handle_string_date(self):
        try:
            if 'T' in self.__date:
                self.__date = self._parse_time_string(self.__date)
            else:
                self.__date = datetime.strptime(self.__date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date string format")
            
    def _parse_time_string(self, time_string):
        if len(time_string.split(':')) == 2:
            return datetime.strptime(time_string + ':00', self.TIMESTAMP_FORMAT)
        elif len(time_string.split(':')) == 1:
            return datetime.strptime(time_string + ':00:00', self.TIMESTAMP_FORMAT)
        else:
            raise ValueError("Invalid time string format")
        
    def _handle_date_date(self):
        self.__date = datetime.combine(self.__date, datetime.min.time())
        
    def _handle_datetime_date(self):
        formatted_date = self.__date.strftime(self.TIMESTAMP_FORMAT)
        if formatted_date != self.__date:
            self.__date = datetime.strptime(formatted_date, self.TIMESTAMP_FORMAT)


