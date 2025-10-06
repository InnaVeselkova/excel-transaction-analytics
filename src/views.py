import json
from typing import Any, Dict

import pandas as pd

from reports import get_expense_report
from src import filter_personal_transfers
from src import (get_currency, get_date_time, get_greeting, get_stocks, read_excel_file, sorted_cards_info,
                 top_transactions)

excel_path = "../data/operations.xlsx"
path = "../data/user_settings.json"
transactions = pd.DataFrame(read_excel_file(excel_path))


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


def get_personal_transfers() -> str:
    """
    Функция возвращающая JSON-строку с транзакциями, содержащими только переводы физ.лицам
    """
    return filter_personal_transfers(read_excel_file(excel_path))


def get_report():
    """
    Функция возвращает траты по заданной категории за последние три месяца (от переданной даты)
    """
    return get_expense_report(transactions, "Переводы", date="2018-03-20 12:11:12")


if __name__ == "__main__":  # pragma: no cover
    print(get_report())
