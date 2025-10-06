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
