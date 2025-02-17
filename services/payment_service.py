from datetime import datetime

import config
from config import hot_price, price, discount


def is_hot_price_date(year: int, month: int, day: int) -> bool:
    """
    :return: True, если текущая дата до или включительно с датой акции, иначе False
    """
    now = datetime.now().date()
    deadline = datetime(year=year, month=month, day=day).date()
    return now <= deadline


def get_final_price_for_user(subscription: bool) -> int:
    final_price = config.price

    if is_hot_price_date(year=2025, month=2, day=19):
        final_price = config.hot_price

    if subscription:
        final_price -= discount

    return final_price