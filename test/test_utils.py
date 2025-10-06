import json
import os
from datetime import date, datetime, timedelta
from unittest.mock import Mock, call, mock_open, patch

import pytest
from dotenv import load_dotenv

from src.utils import (get_currency, get_date_time, get_greeting, get_stocks, read_excel_file, sorted_cards_info,
                       top_transactions)

load_dotenv()

URL = "https://api.apilayer.com/exchangerates_data/convert"
url = "https://www.alphavantage.co/query"
exchange_API = os.getenv('API_KEY')
exchange_API_stock = os.getenv('API_KEY_stocks')

path = "../data/user_settings.json"


def test_read_excel_file_success(sample_excel):
    # Проверка успешного чтения файла
    result = read_excel_file(sample_excel)
    assert isinstance(result, list)
    assert len(result) == 2
    # Проверка содержимого
    assert result[0]['Column1'] == 1
    assert result[0]['Column2'] == 'A'


def test_read_excel_file_not_found():
    # Тест на не найденный файл
    invalid_path = "path/to/nonexistent/file.xlsx"
    result = read_excel_file(invalid_path)
    assert result is None


def test_get_greeting_evening():
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2018, 3, 20, 23, 11, 12)
        greeting = get_greeting()
        assert greeting == "Добрый вечер"


def test_get_greeting_morning():
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2018, 3, 20, 10, 11, 12)
        greeting = get_greeting()
        assert greeting == "Доброе утро"


def test_get_greeting_afternoon():
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2018, 3, 20, 15, 11, 12)
        greeting = get_greeting()
        assert greeting == "Добрый день"


def test_get_greeting_night():
    with patch('src.utils.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2018, 3, 20, 5, 11, 12)
        greeting = get_greeting()
        assert greeting == "Доброй ночи"


def test_get_date_time_default_format():
    data_time = "2023-08-15 14:30:00"
    result = get_date_time(data_time)
    # Первый элемент — первый день месяца, формат DD-MM-YYYY HH:MM:SS
    assert result[0] == "01-08-2023 14:30:00"
    # Второй — исходная дата
    assert result[1] == "15-08-2023 14:30:00"


def test_get_date_time_incorrect_format():
    data_time = "15/08/2023 14:30"
    with pytest.raises(Exception):
        get_date_time(data_time, date_format="%Y-%m-%d %H:%M:%S")


def test_sorted_cards_info_basic():
    data_list = [
        {
            "Дата операции": "2023-08-10",
            "Номер карты": "1234",
            "Сумма операции": 1500
        },
        {
            "Дата операции": "2023-08-15",
            "Номер карты": "5678",
            "Сумма операции": 3000
        },
        {
            "Дата операции": "2023-07-20",
            "Номер карты": "9012",
            "Сумма операции": 2000
        }
    ]

    start_date = "2023-08-01"
    end_date = "2023-08-31"
    time_period = [start_date, end_date]

    result = sorted_cards_info(data_list, time_period)

    # Проверка, что выбраны только записи за август
    assert len(result) == 2
    # Проверка содержимого первой записи
    assert result[0]["last_digits"] == "1234"
    assert result[0]["total_spent"] == 1500
    assert result[0]["cashback"] == 15
    # Проверка второй
    assert result[1]["last_digits"] == "5678"
    assert result[1]["total_spent"] == 3000
    assert result[1]["cashback"] == 30


def test_sorted_cards_info_with_missing_date():
    data_list = [
        {
            "Номер карты": "1234",
            "Сумма операции": 1000
        },
        {
            "Дата операции": "2023-08-10",
            "Номер карты": "5678",
            "Сумма операции": 2000
        }
    ]

    start_date = "2023-08-01"
    end_date = "2023-08-31"
    result = sorted_cards_info(data_list, [start_date, end_date])

    # Вторая запись должна попасть, первая пропущена
    assert len(result) == 1
    assert result[0]["last_digits"] == "5678"
    assert result[0]["total_spent"] == 2000


def test_sorted_cards_info_empty_result():
    data_list = [
        {
            "Дата операции": "2023-07-01",
            "Номер карты": "1234",
            "Сумма операции": 100
        }
    ]
    start_date = "2023-08-01"
    end_date = "2023-08-31"
    result = sorted_cards_info(data_list, [start_date, end_date])
    # Записей в выбранном диапазоне нет
    assert result == []


def test_top_transactions_basic():
    data_list = [
        {"Дата операции": "2023-08-10", "Сумма операции": 1500, "Категория": "еда", "Описание": "обед"},
        {"Дата операции": "2023-08-11", "Сумма операции": 2500, "Категория": "транспорт", "Описание": "такси"},
        {"Дата операции": "2023-08-12", "Сумма операции": 1800, "Категория": "магазин", "Описание": "одежда"},
        {"Дата операции": "2023-08-13", "Сумма операции": 2200, "Категория": "развлечения", "Описание": "кино"},
        {"Дата операции": "2023-08-14", "Сумма операции": 3000, "Категория": "бензин", "Описание": "заправка"},
        {"Дата операции": "2023-08-15", "Сумма операции": 1000, "Категория": "еда", "Описание": "ужин"},
    ]

    result = top_transactions(data_list)

    # Проверка, что возвращены 5 транзакций и их порядок (по убыванию)
    assert len(result) == 5
    assert result[0]["amount"] == 3000
    assert result[1]["amount"] == 2500
    assert result[2]["amount"] == 2200
    assert result[-1]["amount"] == 1500


def test_top_transactions_with_equal_amounts():
    data_list = [
        {"Дата операции": "2023-08-10", "Сумма операции": 2000, "Категория": "еда", "Описание": "обед"},
        {"Дата операции": "2023-08-11", "Сумма операции": 2000, "Категория": "транспорт", "Описание": "такси"},
        {"Дата операции": "2023-08-12", "Сумма операции": 1500, "Категория": "магазин", "Описание": "одежда"},
    ]

    result = top_transactions(data_list)
    # Проверка, что отобрано 3, так как меньше 5
    assert len(result) == 3
    # Сортировка по убыванию суммы
    assert result[0]["amount"] == 2000
    assert result[1]["amount"] == 2000
    assert result[2]["amount"] == 1500


def test_top_transactions_with_missing_keys():
    data_list = [
        {"Дата операции": "2023-08-10", "Сумма операции": 1500},
        {"Дата операции": "2023-08-11"},
        {"Сумма операции": 2000, "Категория": "транспорт"},
    ]

    result = top_transactions(data_list)
    # Проверка, что сортировка происходит, и отсутствующие ключи обрабатываются без ошибок
    assert len(result) <= 3
    # Проверка наличия 'amount' в результатах
    for item in result:
        assert "amount" in item
        assert "date" in item
        assert "category" in item
        assert "description" in item


@patch('requests.get')
def test_get_currency(mock_get):
    # Создаем функцию-обработчик для возврата разного значения json для каждого вызова
    def mock_json():
        # Первый вызов - для USD
        if mock_json.call_count == 0:
            mock_json.call_count += 1
            return {
                "query": {"from": "USD"},
                "result": 83.05
            }
        # Второй вызов - для EUR
        else:
            return {
                "query": {"from": "EUR"},
                "result": 97.14
            }
    mock_json.call_count = 0

    mock_get.return_value.json.side_effect = mock_json

    # Вызов функции
    result = get_currency(path)

    # Проверка результата
    expected = [
        {'currency': 'USD', 'rate': '83.05'},
        {'currency': 'EUR', 'rate': '97.14'}
    ]
    assert result == expected

    # Проверка, что вызовы происходили с правильными параметрами
    calls = [
        call(
            url=URL,
            headers={"apikey": exchange_API},
            params={
                "amount": 1,
                "from": "USD",
                "to": "RUB"
            }
        ),
        call(
            url=URL,
            headers={"apikey": exchange_API},
            params={
                "amount": 1,
                "from": "EUR",
                "to": "RUB"
            }
        )
    ]
    mock_get.assert_has_calls(calls, any_order=True)


@patch('requests.get')
def test_get_stocks_simple(mock_get):
    # Настроим глобальные переменные
    global exchange_API_stock
    exchange_API_stock = 'test_api_key'

    # Тестовые данные, которые будут в файле
    test_data = {
        "user_stocks": ["AAPL", "GOOGL"]
    }

    # Путь к "файлу" — мы замокаем open, чтобы не читать настоящий файл
    path = "fake_path.json"

    # Мокаем открытие файла и json.load, чтобы вернуть тест_data
    with patch("builtins.open", mock_open(read_data=json.dumps(test_data))):

        # Настроим мок response.json() — возвращаем фиксированные данные с нужной датой
        yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        mock_response = Mock()
        mock_response.json.return_value = {
            "Time Series (Daily)": {
                yesterday: {
                    "2. high": "300.00"
                }
            }
        }

        # requests.get всегда возвращает наш mock_response
        mock_get.return_value = mock_response

        # Импорт или определение get_stocks здесь,
        # либо убедитесь, что функция импортирована

        result = get_stocks(path)

        expected = [
            {"stock": "AAPL", "price": 300.00},
            {"stock": "GOOGL", "price": 300.00},
        ]

        assert result == expected
