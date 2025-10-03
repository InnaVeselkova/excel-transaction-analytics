import datetime
import functools
from typing import Optional

import pandas as pd

from src.utils import read_excel_file, logger

excel_path = "../data/operations.xlsx"


def save_report_to_file(filename="Three_monthly_expenses.txt"):
    """
    Функция-декоратор для записи данных в файл
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            logger.info(f"Запись отчета в файл: {filename}")
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(str(result))
                    logger.info(f"Отчет успешно сохранен в {filename}")
            except Exception as e:
                logger.error(f"Ошибка при сохранении файла {filename}: {e}")
            return result
        return wrapper
    return decorator


try:
    transactions = pd.DataFrame(read_excel_file(excel_path))
    logger.info(f"Успешно прочитан файл Excel: {excel_path}, количество записей: {len(transactions)}")
except Exception as e:
    logger.error(f"Ошибка при чтении файла Excel: {excel_path}\n{e}")
    transactions = pd.DataFrame()  # создаем пустой DataFrame в случае ошибки


def spending_by_category(transactions: pd.DataFrame,
                         category: str,
                         date: Optional[str] = None) -> pd.DataFrame:
    """
    Функция, которая возвращает сумму затрат по заданной категории за последние три месяца
    от указанной даты (или текущей, если дата не указана).
    """
    logger.info(f"Вычисление затрат по категории '{category}' за последние 3 месяца до даты: {date}")

    if date is None:
        date = datetime.datetime.now()
        logger.debug("Дата не указана, используется текущая дата")
    else:
        date = pd.to_datetime(date)
        logger.debug(f"Обрабатываемая дата: {date}")

    three_months_ago = date - pd.DateOffset(months=3)

    # Конвертация датафрейма в удобный формат
    try:
        transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)
        logger.info("Дата операций успешно конвертирована в datetime")
    except Exception as e:
        logger.error(f"Ошибка при преобразовании даты операций: {e}")

    # Фильтрация по категории и дате
    filtered = transactions[
        (transactions['Категория'] == category) &
        (transactions['Дата операции'] >= three_months_ago) &
        (transactions['Дата операции'] <= date)
        ]
    total_expenses = filtered['Сумма операции'].sum()
    logger.info(f"Общая сумма затрат по категории '{category}': {total_expenses}")
    return total_expenses


@save_report_to_file()
def get_expense_report(transactions, category, date=None):
    logger.info(f"Генерация отчета по категории '{category}', дата: {date}")
    total = spending_by_category(transactions, category, date)
    report_ = f"Общие расходы по категории '{category}' за последние 3 месяца: {total}"
    logger.info("Отчет сформирован")
    return report_


if __name__ == "__main__":
    report = get_expense_report(transactions, "Переводы", date="2018-03-20 12:11:12")
    print(report)
