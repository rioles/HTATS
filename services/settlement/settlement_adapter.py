from abc import ABC, abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List, Optional, TypeVar
from models import storage
from models.settlement import Settlement
from services.settlement.settlement_port import SettlementInterface


T = TypeVar('T')  # Type variable for the current class


class SettlementAdapter(SettlementInterface):
    def get_sum_with_intervall(
        self,
        **object_meta_data: Dict[str, str]
    ) -> Dict[str, str]:
        
        current_datetime = datetime.now()
        start_day = current_datetime.replace(hour=0, minute=0, second=0, microsecond=0)
        sum_amount = storage.get_sum_with_filter_and_interval(Settlement, start_day, current_datetime, "settlement_amount", **{"user_id":object_meta_data["user_id"]})
        return {"total_amoun":sum_amount}