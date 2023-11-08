from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class DateValue:
    __date: Optional[datetime] = None
    TIMESTAMP_FORMAT = "%Y-%m-%dT%H:%M:%S"

    def __post_init__(self):
        self._check_date()

    @property
    def date(self):
        return self.__date.strftime(self.TIMESTAMP_FORMAT) if self.__date is not None else None

    def _check_date(self):
        if self.__date is None:
            raise ValueError("Date should not be None")
        elif isinstance(self.__date, str):
            try:
                if 'T' in self.__date:
                    self.__date = datetime.strptime(self.__date, self.TIMESTAMP_FORMAT)
                else:
                    self.__date = datetime.strptime(self.__date, "%Y-%m-%d")
            except ValueError:
                raise ValueError("Invalid date string format")
        elif isinstance(self.__date, datetime):
            formatted_date = self.__date.strftime(self.TIMESTAMP_FORMAT)
            if formatted_date != self.__date:
                self.__date = datetime.strptime(formatted_date, self.TIMESTAMP_FORMAT)
        elif isinstance(self.__date, date):
            self.__date = datetime.combine(self.__date, datetime.min.time())

