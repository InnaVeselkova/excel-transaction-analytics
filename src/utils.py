import pandas as pd
import json

excel_path="../data/operations.xlsx"

def read_excel_file(excel_path):
    # Функция чтения Excel-файла
    try:
        df = pd.read_excel(excel_path)
        return df
    except FileNotFoundError:
        print("Файл не найден.")
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
    return None


def excel_to_json(data):
    # Функция преобразования файла из excel в json
    # Преобразование DataFrame в список словарей
    data_list = df.to_dict(orient='records')
    # Преобразование списка в JSON-строку
    json_data = json.dumps(data_list, ensure_ascii=False, indent=4)
    # Запись JSON в файл
    with open('operations.json', 'w', encoding='utf-8') as operation_json:
        operation_json.write(json_data)
    return json_data


if __name__ == "__main__":
    df = read_excel_file(excel_path)
    if df is not None:
        data = excel_to_json(df)
        print(data)
