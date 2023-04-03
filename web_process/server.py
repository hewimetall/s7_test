import sqlite3

from fastapi import FastAPI

import db
from db import get_db

app = FastAPI()


@app.get("/flights/{flight_date}")
def get_flights(flight_date: str):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    rows = db.get_flights_by_date(conn, flight_date)
    conn.close()
    return rows
