import csv
from typing import Dict, List, Union


def csv_to_json(file_path: str) -> Dict[str, Union[str, int, List[Dict[str, str]]]]:
    # Извлекаем номер рейса и аэропорт вылета из имени файла
    filename = file_path.split('/')[-1]
    flt, dep = filename.split('_')[1:3]

    # Читаем данные из csv-файла
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        data = [row for row in reader]

    # Формируем словарь
    json_data = {
        'flt': int(flt),
        'date': filename[:8],
        'dep': dep[:-4],
        'prl': data
    }

    return json_data
