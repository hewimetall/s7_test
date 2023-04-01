from fastapi import FastAPI
import sqlite3

from .db import get_db

app = FastAPI()

@app.get("/flights/{flight_date}")
def get_flights(flight_date: str):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    query = f"SELECT * FROM flight WHERE flight_date='{flight_date}'"
    cursor = conn.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return rows
