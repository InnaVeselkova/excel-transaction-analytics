import pytest
import pandas as pd


@pytest.fixture
def sample_excel():
    file_path = "../data/sample.xlsx"
    df = pd.DataFrame({
        'Column1': [1, 2],
        'Column2': ['A', 'B']
    })
    df.to_excel(file_path, index=False)

    return file_path


@pytest.fixture
def sample_transactions():
    data = {
        'Дата операции': [
            '01/01/2023', '15/02/2023', '10/04/2023', '20/05/2023',
            '01/06/2023', '15/07/2023'
        ],
        'Категория': [
            'Food', 'Food', 'Transport', 'Food', 'Transport', 'Food'
        ],
        'Сумма операции': [
            50, 30, 20, 100, 15, 25
        ]
    }
    df = pd.DataFrame(data)
    return df
