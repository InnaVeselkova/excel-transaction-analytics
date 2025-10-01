import json
import re
from typing import List, Dict
from src.utils import read_excel_file

excel_path = "../data/operations.xlsx"


def filter_personal_transfers(data_list: List[Dict]) -> List[Dict]:
    """
    Функция фильтрует транзакции, относящиеся к переводам физлицам
    """

    pattern = re.compile(r'\b[А-ЯЁ][а-яё]+ [А-ЯЁ]\.')

    filtered = [
        transaction for transaction in data_list
        if transaction.get('Категория') == 'Переводы' and pattern.search(transaction.get('Описание', ''))
        ]

    return json.dumps(filtered, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    print(filter_personal_transfers(read_excel_file(excel_path)))
