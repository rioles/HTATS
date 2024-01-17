from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, TypeVar
T = TypeVar('T')  # Type variable for the current class


class SettlementPort(ABC):
    @abstractmethod
    def get_sum_with_intervall(
        self,
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Calculate the sum of settlement amounts within a specified interval.

        Parameters:
        - object_meta_data (Dict[str, str]): Metadata including "user_id".

        Returns:
        - Dict[str, float]: {"total_amount": sum_amount}
        """
        
    @abstractmethod
    def get_settlement_list_by_criteria(
        self, 
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        pass
    
    """
    @abstractmethod
    def get_invoice_list_by_criteria(
        self, 
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        pass
    """
    @abstractmethod
    def get_all_invoice_list_by_criteria(
        self, 
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_all_settlement_list_by_criteria(
        self, 
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def get_unpaid_invoice_list_by_criteria(
        self, 
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, Any]:
        pass