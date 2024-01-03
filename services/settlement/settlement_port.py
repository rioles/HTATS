from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar
T = TypeVar('T')  # Type variable for the current class


class SettlementPort(ABC):
    @abstractmethod
    def get_sum_with_intervall(
        self
    ) -> Dict[str, str]:
        pass