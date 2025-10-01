import json
from src.utils import (get_greeting, get_date_time, read_excel_file, sorted_cards_info, top_transactions, get_currency,
                       get_stocks)
from typing import Dict, Any


excel_path="../data/operations.xlsx"
path = "../data/user_settings.json"


def get_main_info(date_time: str) -> Dict[str, Any]:
    """
    Функция, принимающая на вход строку с датой и временем в формате
    YYYY-MM-DD HH:MM:SS и возвращающая JSON-ответ
    """

    greeting = get_greeting()
    time_period = get_date_time(date_time)
    data_list = read_excel_file(excel_path)
    card_info = sorted_cards_info(data_list, time_period)
    top_five = top_transactions(data_list)
    currency = get_currency(path)
    stock_prices = get_stocks(path)

    data = {
        "greeting": greeting,
        "cards": card_info,
        "top_transactions": top_five,
        "currency_rates": currency,
        "stock_prices": stock_prices
        }

    data_json = json.dumps(data, ensure_ascii=False, indent=4)

    return data_json
