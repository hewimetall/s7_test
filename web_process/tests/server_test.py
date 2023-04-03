import os
import sqlite3
import unittest

from fastapi.testclient import TestClient

import db
from web_process.server import app


class TestGetFlights(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        db.init()

    def tearDown(self):
        os.remove("s7.db")

    def test_get_flights_with_valid_date(self):
        response = self.client.get("/flights/2022-01-01")
        self.assertEqual(response.status_code, 200)
        conn = sqlite3.connect("s7.db")
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT * FROM flight WHERE depdate='2022-01-01'")
        rows = cursor.fetchall()
        conn.close()
        self.assertEqual(len(response.json()), len(rows))

    def test_get_flights_with_invalid_date(self):
        response = self.client.get("/flights/2022-02-31")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 0)

    def test_get_flights_with_no_date(self):
        response = self.client.get("/flights/")
        self.assertEqual(response.status_code, 404)
