from dataclasses import dataclass
from typing import Optional
import re

@dataclass(frozen=True)
class EmailAddress:
  _address: Optional[str] = None

  def __post_init__(self):
    if self._address:
      self.validate_address()

  @property
  def email(self):
    return self._address

  def validate_address(self):
    # Email address validation using regex (consider a stricter pattern if needed)
    email_pattern = re.compile(r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$')
    if self._address and not email_pattern.match(self._address):
      raise ValueError("Invalid email address")

  def __eq__(self, other):
    if isinstance(other, EmailAddress):
      return self._address == other._address
    return False
