from dataclasses import dataclass
import re

@dataclass(frozen=True)
class EmailAddress:
    _address: str

    def __post_init__(self):
        self.validate_address()

    @property
    def email(self):
        return self._address

    def validate_address(self):
        # Email address validation using regex
        email_pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
        if not email_pattern.match(self._address):
            raise ValueError("Invalid email address")

    def __eq__(self, other):
        if isinstance(other, EmailAddress):
            return self.address == other.address
        return False


