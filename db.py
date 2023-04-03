import logging
import sqlite3
from datetime import date
from typing import List

import settings

logger = logging.getLogger("sqlite")


def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.DATABASE)
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


def insert_flight(conn: sqlite3.Connection, file_name: str, flt: int, dep: str, depdate: date) -> None:
    """
    Добавляет новую запись в таблицу 'flight'
    """
    c = conn.cursor()
    c.execute("INSERT INTO flight (file_name, flt, dep, depdate) VALUES (?, ?, ?, ?)",
              (file_name, flt, dep, depdate))
    conn.commit()


def get_flights_by_date(conn: sqlite3.Connection, date: date) -> List[dict]:
    """
    Выбирает все записи из таблицы 'flight', соответствующие заданной дате
    """
    c = conn.cursor()
    c.execute("SELECT * FROM flight WHERE depdate=?", (date,))
    rows = c.fetchall()
    return [{'id': row[0], 'file_name': row[1], 'flt': row[2], 'dep': row[3], 'depdate': row[4]} for row in rows]


def delete_row(conn: sqlite3.Connection, file_name: str, date: date):
    c = conn.cursor()
    c.execute("DELETE FROM flight WHERE depdate=? AND file_name=?", (date, file_name))
    conn.commit()


def init() -> bool:
    cur = get_db()
    is_good = True
    try:
        create_flight_table(cur)
    except Exception as e:
        logger.error(e)
        is_good = False
    finally:
        cur.close()
    return is_good
