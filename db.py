import sqlite3
from typing import List
from datetime import datetime
def get_db():
    conn = sqlite3.connect("flights.db")
    return conn

def create_flight_table(conn: sqlite3.Connection) -> None:
    """
    Создает таблицу 'flight' в базе данных
    """
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS flight
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  file_name TEXT NOT NULL,
                  flt INTEGER NOT NULL,
                  depdate DATE NOT NULL,
                  dep TEXT NOT NULL)''')
    conn.commit()

def insert_flight(conn: sqlite3.Connection, file_name: str, flt: int, dep: str, depdate: datetime) -> None:
    """
    Добавляет новую запись в таблицу 'flight'
    """
    c = conn.cursor()
    c.execute("INSERT INTO flight (file_name, flt, dep, depdate) VALUES (?, ?, ?, ?)",
              (file_name, flt, dep, depdate.date()))
    conn.commit()


def get_flights_by_date(conn: sqlite3.Connection, date: datetime) -> List[dict]:
    """
    Выбирает все записи из таблицы 'flight', соответствующие заданной дате
    """
    c = conn.cursor()
    c.execute("SELECT * FROM flight WHERE depdate=?", (date.date(),))
    rows = c.fetchall()
    return [{'id': row[0], 'file_name': row[1], 'flt': row[2], 'dep': row[3], 'depdate': row[4]} for row in rows]
