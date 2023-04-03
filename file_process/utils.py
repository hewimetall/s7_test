import csv
import json
import os
from datetime import datetime
from typing import Dict, List, Union

import db
from schema import FlightFromName


def convert_date(date_string: str) -> str:
    # Извлекаем год, месяц и день из строки
    year = int('19' + date_string[5:7])
    month = datetime.strptime(date_string[2:5], '%b').month
    day = int(date_string[:2])

    # Формируем новую дату в формате YYYY-MM-DD
    new_date = datetime(year, month, day).strftime('%Y-%m-%d')

    return new_date


def csv_to_json(file_path: str) -> Dict[str, Union[str, int, List[Dict[str, str]]]]:
    # Извлекаем номер рейса и аэропорт вылета из имени файла
    filename = file_path.split('/')[-1]
    flt, dep = filename.split('_')[1:3]

    # Читаем данные из csv-файла
    with open(file_path, 'r') as f:
        reader = csv.DictReader(f, delimiter=';')
        data = []
        for row in reader:
            row['bdate'] = convert_date(row['bdate'])
            data.append(row)

    date = filename[:8]
    # Формируем словарь
    json_data = {
        'flt': int(flt),
        'date': f"{date[:4]}-{date[4:6]}-{date[6:]}",
        'dep': dep[:-4],
        'prl': data
    }

    return json_data


def parsing_to_db(flight: FlightFromName) -> bool:
    # Извлекаем номер рейса и аэропорт вылета из имени файла
    con = db.get_db()
    db.insert_flight(con, flight.filename, flight.flt, flight.dep, flight.date)
    con.close()
    return True


def parsint_to_file(flight: FlightFromName) -> bool:
    json_data = csv_to_json(str(flight.file_path.full_path))
    if os.path.exists(flight.file_path.path_out()):
        return False
    with open(flight.file_path.path_out(), "w") as f:
        json.dump(json_data, f)
    return True


def test_dirs(test_path: str):
    if not os.path.isdir(test_path):
        raise Exception(f"{test_path} must be a directory")

    if not os.access(test_path, os.R_OK | os.W_OK):
        raise Exception(f"{test_path} must be a permissions RW")

    return True
