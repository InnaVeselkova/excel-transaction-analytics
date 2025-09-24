from src.views import get_greeting
from src.utils import excel_to_json, read_excel_file

excel_path="../data/operations.xlsx"

greeting = input(get_greeting())
print(greeting)

df = read_excel_file(excel_path)
if df is not None:
    data_json = excel_to_json(df)


