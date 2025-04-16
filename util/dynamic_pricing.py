import logging
from datetime import date
from typing import Optional

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def calculate_dynamic_price(base_price: float, check_in: Optional[date]) -> float:
    if not check_in:
        return base_price
    if check_in.month in [7, 8]:
        return round(base_price * 1.2, 2)
    elif check_in.month in [1, 2, 11]:
        return round(base_price * 0.9, 2)
    else:
        return base_price
