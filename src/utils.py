import json
import os
import logging
from datetime import date, datetime, timedelta
from pprint import pprint
from typing import Any, Dict, List

import pandas as pd
import requests
from dotenv import load_dotenv

# Настройка логгера
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

path = "../data/user_settings.json"
excel_path = "../data/operations.xlsx"

URL = "https://api.apilayer.com/exchangerates_data/convert"

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
        logger.info(f"Чтение Excel файла по пути: {excel_path}")
        df = pd.read_excel(excel_path)
        # Преобразование DataFrame в список словарей
        data_dict = df.to_dict(orient='records')
        logger.info(f"Успешно прочитано {len(data_dict)} записей из Excel.")
        return data_dict
    except FileNotFoundError:
        logger.error("Файл не найден.")
        print("Файл не найден.")
    except Exception as e:
        logger.error(f"Ошибка при чтении файла: {e}")
        print(f"Произошла ошибка при чтении файла: {e}")
    return None


def get_greeting():
    """
    Функция для определения приветствия, соответствующего времени суток
    """
    hour = datetime.now().hour
    logger.debug(f"Определение приветствия для часа: {hour}")
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
    logger.debug(f"Парсинг даты: {data_time} формата {date_format}")
    dt = datetime.strptime(data_time, date_format)
    start_date = dt.replace(day=1)

    period = [start_date.strftime("%d-%m-%Y %H:%M:%S"), dt.strftime("%d-%m-%Y %H:%M:%S")]
    logger.info(f"Период дат: {period}")
    return period


def sorted_cards_info(data_list: List[Dict[str, Any]], time_period: List) -> List[Dict]:
    """
    Функция для получения информации по картам за определенный диапазон дат
    """
    logger.info("Начинаем фильтрацию и обработку информации по картам")
    result = []

    for record in data_list:
        payment_date = record.get("Дата операции")
        if payment_date is None:
            logger.warning("Пропущена запись без даты операции")
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
    logger.info(f"Отобрано {len(result)} записей по картам.")
    return result


def top_transactions(data_list: List[Dict[str, Any]]) -> List[Dict]:
    """
    Функция для получения 5 транзакций с наибольшей суммой
    """
    logger.info("Определение 5 транзакций с наибольшей суммой")
    try:
        sorted_cards = sorted(data_list, key=lambda x: x["Сумма операции"], reverse=True)
        result_five = sorted_cards[:5]

        result = []

        for record in result_five:
            info = {
                "date": record.get("Дата операции", ""),
                "amount": record.get("Сумма операции", 0),
                "category": record.get("Категория", ""),
                "description": record.get("Описание", "")
            }
            result.append(info)
        logger.info(f"Получено {len(result)} топ транзакций.")
        return result
    except Exception as e:
        logger.error(f"Ошибка при сортировке транзакций: {e}")
        return []


currency_data = []


def get_currency(path: str) -> List[Dict]:
    """
    Функция, возвращающая курс валют
    """
    logger.info("Получение курсов валют")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            for currency in data["user_currencies"]:
                params = {
                    "amount": 1,
                    "from": f"{currency}",
                    "to": "RUB"
                }
                headers = {
                    "apikey": exchange_API
                }
                logger.debug(f"Запрос курса валюты {currency}")
                response = requests.get(url=URL, headers=headers, params=params)
                result = response.json()
                result_currency = result["query"]["from"]
                result_rate = round(result["result"], 2)
                currency_data.append({
                    "currency": f"{result_currency}",
                    "rate": f"{result_rate}"
                })
            logger.info(f"Получено курсов валют: {len(currency_data)}")
        return currency_data
    except Exception as e:
        logger.error(f"Ошибка при получении курса валют: {e}")
        return []


def get_stocks(path: str) -> List[Dict]:
    """
    Функция, возвращающая курс акций
    """
    logger.info("Получение курсов акций")
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            stocks = []
            for stock in data["user_stocks"]:
                yesterday = date.today() - timedelta(days=1)
                url = "https://www.alphavantage.co/query"
                params = {
                    "function": "TIME_SERIES_DAILY",
                    "symbol": f"{stock}",
                    "apikey": exchange_API_stock
                }

                response = requests.get(url=url, params=params)
                result = response.json()
                pprint(result)
                result_price = round(float(result['Time Series (Daily)'][yesterday]["2. high"]), 2)
                stocks.append({
                    "stock": stock,
                    "price": result_price
                })
        return stocks
    except Exception as e:
        logger.error(f"Ошибка при получении курсов акций: {e}")
        return []


if __name__ == "__main__":
    print(read_excel_file(excel_path))
