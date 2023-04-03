import datetime
import os
import shutil
import tempfile
import unittest
from unittest.mock import patch, mock_open, ANY

import db
from file_process.utils import csv_to_json, parsing_to_db, parsint_to_file, test_dirs, convert_date
from schema import FlightFromName


class TestFileProcessUtils(unittest.TestCase):
    def setUp(self) -> None:
        db.init()

    def tearDown(self):
        os.remove("s7.db")

    def test_convert_bdate(self):
        inp = "11NOV73"
        output = '1973-11-11'
        self.assertEqual(convert_date(inp), output)

    def test_csv_to_json(self):
        file_path = "test/in/20221129_1234_DME.csv"
        expected_output = {
            'flt': 1234,
            'date': "2022-11-29",
            'dep': 'DME',
            'prl': [
                {
                    "num": "1",
                    "surname": "IVANOV",
                    "firstname": "IVAN",
                    "bdate": "1973-11-11"
                },
            ]
        }
        with patch("builtins.open", mock_open(read_data="num;surname;firstname;bdate\n1;IVANOV;IVAN;11NOV73\n")):
            output = csv_to_json(file_path)

        self.assertEqual(output, expected_output)

    def test_parsing_to_db_simple(self):
        with patch("file_process.utils.db.get_db") as mock_db:
            with patch("file_process.utils.db.insert_flight") as mock_insert:
                flight = FlightFromName.to_python("/test/in/20221129_1234_DME.csv")
                output = parsing_to_db(flight)
        mock_insert.assert_called_with(ANY, "20221129_1234_DME.csv", 1234, "DME", datetime.date(2022, 11, 29))
        self.assertTrue(output)

    def test_parsing_to_db(self):
        flight = FlightFromName.to_python("/test/in/20221129_1234_DME.csv")
        output = parsing_to_db(flight)
        con = db.get_db()
        self.assertEqual(len(db.get_flights_by_date(con, datetime.date(2022, 11, 29))), 1)
        con.close()
        self.assertTrue(output)

    def test_parsint_to_file(self):
        with tempfile.TemporaryDirectory() as temp:
            os.mkdir(temp + "/out")
            with patch("file_process.utils.csv_to_json", return_value={}):
                flight = FlightFromName.to_python(temp + "/in/20221129_1234_DME.csv")
                output = parsint_to_file(flight)
            self.assertTrue(os.path.isfile(temp + "/out/" + "20221129_1234_DME.json"))
            self.assertTrue(output)

    def test_test_dirs(self):
        test_path = "test_dir"
        os.makedirs(test_path)

        with self.subTest(msg="Test directory is a directory"):
            self.assertTrue(test_dirs(test_path))

        with self.subTest(msg="Test directory has permissions RW"):
            os.chmod(test_path, 0o700)
            self.assertTrue(test_dirs(test_path))

        with self.subTest(msg="Test directory is not a directory"):
            self.assertRaisesRegex(Exception, "must be a directory", test_dirs, "test_file")

        with self.subTest(msg="Test directory has no permissions RW"):
            os.chmod(test_path, 0o400)
            self.assertRaisesRegex(Exception, "must be a permissions RW", test_dirs, test_path)
        shutil.rmtree(test_path)
