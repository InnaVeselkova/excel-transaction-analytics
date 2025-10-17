import json
import re
from typing import Dict, List

from src.utils import read_excel_file, logger


def filter_personal_transfers(data_list: List[Dict]) -> str:
    """
    Функция фильтрует транзакции, относящиеся к переводам физлицам
    """

    logger.info("Начало фильтрации транзакций по категориям и описанию.")
    pattern = re.compile(r'\b[А-ЯЁ][а-яё]+ [А-ЯЁ]\.')

    try:
        filtered = [
            transaction for transaction in data_list
            if transaction.get('Категория') == 'Переводы' and pattern.search(transaction.get('Описание', ''))
        ]
        logger.info(f"Отфильтровано транзакций: {len(filtered)} из {len(data_list)}.")
    except Exception as e:
        logger.error(f"Ошибка при фильтрации транзакций: {e}")
        raise

    result_json = json.dumps(filtered, ensure_ascii=False, indent=2)
    logger.info("Фильтрация завершена.")
    return result_json
