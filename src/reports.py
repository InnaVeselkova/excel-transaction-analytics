import datetime
import functools
from typing import Optional

import pandas as pd

from src.utils import read_excel_file

excel_path = "../data/operations.xlsx"


def save_report_to_file(filename="Three_monthly_expenses.txt"):
    """
    Функция-декоратор для записи данных в файл
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(str(result))
            return result
        return wrapper
    return decorator


transactions = pd.DataFrame(read_excel_file(excel_path))


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция, которая возвращает сумму затрат по заданной категории за последние три месяца
    от указанной даты (или текущей, если дата не указана).
    """

    if date is None:
        date = datetime.datetime.now()
    else:
        date = pd.to_datetime(date)

    three_months_ago = date - pd.DateOffset(months=3)

    # Конвертация датафрейма в удобный формат
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)

    # Фильтрация по категории и дате
    filtered = transactions[
        (transactions['Категория'] == category) &
        (transactions['Дата операции'] >= three_months_ago) &
        (transactions['Дата операции'] <= date)
        ]
    total_expenses = filtered['Сумма операции'].sum()
    return total_expenses


@save_report_to_file()
def get_expense_report(transactions, category, date=None):
    total = spending_by_category(transactions, category, date)
    return f"Общие расходы по категории '{category}' за последние 3 месяца: {total}"


if __name__ == "__main__":
    report = get_expense_report(transactions, "Переводы", date="2018-03-20 12:11:12")
    print(report)
