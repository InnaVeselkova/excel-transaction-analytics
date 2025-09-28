import pandas as pd
import requests
from dotenv import load_dotenv
import json
import os
from typing import List, Dict, Any
from datetime import datetime
from datetime import date


path = "../data/user_settings.json"
excel_path = "../data/operations.xlsx"

URL = f"https://api.apilayer.com/exchangerates_data/convert"

# Загрузка переменных из .env-файла
load_dotenv()

# Получение значения переменной exchange_API из .env-файла
exchange_API = os.getenv('API_KEY')
exchange_API_stock = os.getenv('API_KEY_stocks')


def read_excel_file(excel_path) -> List[Dict]:
    """
    Функция чтения Excel-файла и преобразования в список словарей
    """
    try:
        df = pd.read_excel(excel_path)
        # Преобразование DataFrame в список словарей
        data_dict = df.to_dict(orient='records')
        return data_dict
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
    return None


def get_greeting():
    """
    Функция для определения приветствия, соответствующего времени суток
    """
    hour = datetime.now().hour
    if 0 <= hour < 6:
        return "Доброй ночи"
    elif 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    else:
        return "Добрый вечер"


def get_date_time(data_time: str, date_format: str = "%Y-%m-%d %H:%M:%S") -> List[str]:
    """
    Функция для определения периода дат, по которым нужно получить информацию
    """
    dt = datetime.strptime(data_time, date_format)
    start_date = dt.replace(day=1)

    return [
        start_date.strftime("%d-%m-%Y %H:%M:%S"),
        dt.strftime("%d-%m-%Y %H:%M:%S")
    ]


def sorted_cards_info(data_list: List[Dict[str, Any]], time_period: List) -> List[Dict]:
    """
    Функция для получения информации по картам за определенный диапазон дат
    """
    result = []

    for record in data_list:
        payment_date= record.get("Дата операции")
        if payment_date is None:
            continue

        start_date, end_date = time_period
        if start_date <= payment_date <= end_date:
            total_spent = record.get("Сумма операции", 0)
            cashback = total_spent // 100
        # Собираем информацию по карте
            info = {
                "last_digits": record.get("Номер карты", ""),
                "total_spent": total_spent,
                "cashback": cashback
            }
            result.append(info)

    return result


def top_transactions(data_list: List[Dict[str, Any]]) -> List[Dict]:
    """
    Функция для получения 5 транзакций с наибольшей суммой
    """
    sorted_cards = sorted(data_list, key=lambda x: x["Сумма операции"], reverse=True)
    result_five = sorted_cards [:5]

    result = []

    for record in result_five:
        info = {
            "date": record.get("Дата операции", ""),
            "amount": record.get("Сумма операции", 0),
            "category": record.get("Категория", ""),
            "description": record.get("Описание", "")
        }
        result.append(info)
    return result


currency_data = []


def get_currency(path: str) -> List[Dict]:
    """
    Функция, возвращающая курс валют
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for currency in data["user_currencies"]:
            params ={
                "amount": 1,
                "from": f"{currency}",
                "to": "RUB"
            }
            headers = {
                "apikey": exchange_API
            }
            response = requests.get(url=URL, headers=headers, params=params)
            result = response.json()
            result_currency = result["query"]["from"]
            result_rate = round(result["result"], 2)
            currency_data.append({
                "currency": f"{result_currency}",
                "rate": f"{result_rate }"
            })
        return currency_data


def get_stocks(path: str) -> List[Dict]:
    """
    Функция, возвращающая курс акций
    """
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for stock in data["user_stocks"]:
            today = date.today()
            url = f"https://www.alphavantage.co/query"
            params = {
                "function": today,
                "symbol": f"{stock}",
                "interval": "5min"
            }
            headers = {
                "apikey": exchange_API_stock
            }

            response = requests.get(url=url, headers=headers, params=params)
            result = response.json()
            print(result)


        return data


if __name__ == "__main__":
    get_stocks(path)



