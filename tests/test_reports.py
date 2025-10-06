import datetime

import pandas as pd

from src.reports import get_expense_report, spending_by_category


def test_get_expense_report_recent_category(sample_transactions):
    # Установка даты, чтобы проверить фильтр
    test_date = datetime.datetime(2023, 7, 15)
    category = 'Food'

    report = get_expense_report(sample_transactions, category, date=test_date)
    # Проверка суммы
    expected_total = 125
    expected_report = f"Общие расходы по категории '{category}' за последние 3 месяца: {expected_total}"
    assert report == expected_report


def test_get_expense_report_no_data_for_category(sample_transactions):
    # Тест на несуществующую категорию
    report = get_expense_report(sample_transactions, 'Nonexistent', date='2023-07-15')
    assert '0' in report  # сумма должна быть 0


def test_spending_by_category_calculation(sample_transactions):
    # Тест отдельной функции
    total = spending_by_category(pd.DataFrame(sample_transactions), 'Food', '2023-07-15')
    assert total == 125  # 50 + 30 + 25


def test_spending_by_category_without_date(sample_transactions):
    # Проверка по текущей дате, не имеет значения для теста
    total = spending_by_category(pd.DataFrame(sample_transactions), 'Transport')
    # В данных только одна строка 'Transport', которая в апреле или июне
    assert total >= 0  # просто проверить, что не исключение
