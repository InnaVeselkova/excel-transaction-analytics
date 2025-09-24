import json
from datetime import datetime

# Функция для определения приветствия
def get_greeting():
    hour = datetime.now().hour
    if 0 <= hour < 6:
        return "Доброй ночи"
    elif 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 17:
        return "Добрый день"
    else:
        return "Добрый вечер"


# Функция получения данных по картам
def transactions_data (data_json):
    response = []
    for transaction in data_json:
        transaction.get("Номер карты").append(response)
