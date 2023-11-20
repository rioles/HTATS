import re
from dataclasses import dataclass

@dataclass(frozen=True)
class PhoneNumber:
    _number: str

    def __post_init__(self):
        self.validate_number()

    @property
    def phone_number(self):
        return self._number

    def validate_number(self):
        if not self._number.isdigit():
            raise ValueError("Invalid phone number. Must contain only digits.")

    def __eq__(self, other):
        if isinstance(other, PhoneNumber):
            return self.number == other.number
        return False
