import json

import pytest

from src import filter_personal_transfers


@pytest.mark.parametrize(
    "input_data, expected_count, description_keywords",
    [
        (
            # Тестовые данные, где есть подходящие транзакции
            [
                {'Категория': 'Переводы', 'Описание': 'Иванов А. перевел деньги'},
                {'Категория': 'Переводы', 'Описание': 'Петров В. перевод'},
                {'Категория': 'Переводы', 'Описание': 'Некорректное описание'},
            ],
            2,  # ожидаемое количество отфильтрованных транзакций
            ['Иванов А.', 'Петров В.']
        ),
        (
            # Тестовые данные, где нет подходящих транзакций
            [
                {'Категория': 'Переводы', 'Описание': 'Покупка'},
                {'Категория': 'Другие', 'Описание': 'Иванов А.'}
            ],
            0,
            []
        ),
        (
            # Данные без транзакций
            [],
            0,
            []
        ),
        (
            # Транзакции с неправильной категорией
            [
                {'Категория': 'Покупки', 'Описание': 'Иванов А.'}
            ],
            0,
            []
        ),
        (
            # Транзакции с описанием, не соответствующие шаблону
            [
                {'Категория': 'Переводы', 'Описание': 'Что-то другое'}
            ],
            0,
            []
        ),
    ]
)
def test_filter_personal_transfers_parametrized(input_data, expected_count, description_keywords):
    result_json = filter_personal_transfers(input_data)
    result = json.loads(result_json)
    assert len(result) == expected_count
    for transaction in result:
        if description_keywords:
            description = transaction['Описание']
            assert any(keyword.split()[0] in description for keyword in description_keywords)
        else:
            # если нет ожидаемых транзакций, список должен быть пустой
            assert True
