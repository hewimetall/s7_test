import os
import queue
import shutil
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

import db
import file_handler
from file_process import utils
from file_process.worker import StepHelper, Worker


def gen_struct(tmp):
    dirs = [
        "in",
        "out",
        "ok",
        "err"
    ]
    for dir in dirs:
        file_handler.create_directory(f"{tmp}/{dir}")


class TestStepHelper(unittest.TestCase):

    def setUp(self):
        db.init()
        self.tmp_dir = tempfile.mkdtemp()
        gen_struct(self.tmp_dir)
        self.filename = "20221129_1234_DME.csv"
        self.file_path = self.tmp_dir + '/in/' + self.filename
        self.data_file = """num;surname;firstname;bdate\n1;IVANOV;IVAN;11NOV73\n2;PETROV;ALEXANDER;13JUL79\n3;BOSHIROV;RUSLAN;12APR78"""
        with open(self.file_path, "w") as f:
            f.write(self.data_file)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
        os.remove("s7.db")

    def test_start_success(self):
        self.helper = StepHelper(self.file_path)

        with patch("file_process.utils.parsint_to_file", return_value=True):
            with patch("file_process.utils.parsing_to_db", return_value=True):
                self.helper.start()
                self.assertEqual(self.helper.status, StepHelper.Status.SUCCESS)

    def test_start_fail_parseint_to_file(self):
        self.helper = StepHelper(self.file_path)

        with patch("file_process.utils.parsint_to_file", return_value=False):
            with patch("file_process.utils.parsing_to_db", return_value=True):
                self.helper.start()
                self.assertEqual(self.helper.status, StepHelper.Status.FAIL)

    def test_start_fail_parsing_to_db(self):
        self.helper = StepHelper(self.file_path)

        with patch("file_process.utils.parsint_to_file", return_value=True):
            with patch("file_process.utils.parsing_to_db", return_value=False):
                self.helper.start()
                self.assertEqual(self.helper.status, StepHelper.Status.FAIL)

    def test_fail(self):
        self.helper = StepHelper(self.file_path)

        with patch("db.delete_row") as mock_delete:
            with patch("file_handler.move_file") as mock_move:
                self.helper.fail()
                self.assertEqual(mock_delete.call_count, 1)
                self.assertEqual(mock_move.call_count, 1)
                self.assertEqual(self.helper.status, StepHelper.Status.FINISH)

    def test_fail_row(self):
        self.helper = StepHelper(self.file_path)

        utils.parsing_to_db(self.helper.flight)
        with patch("file_handler.move_file") as mock_move:
            self.helper.fail()
            self.assertEqual(mock_move.call_count, 1)
            self.assertEqual(self.helper.status, StepHelper.Status.FINISH)

        con = db.get_db()
        self.assertEqual(len(db.get_flights_by_date(con, self.helper.flight.date)), 0)
        con.close()

    def test_success(self):
        self.helper = StepHelper(self.file_path)
        source_path = self.tmp_dir + '/in/' + self.filename
        target_dir = self.tmp_dir + '/ok'
        with patch("file_handler.move_file") as mock_move_file:
            self.helper.success()
            mock_move_file.assert_called_once_with(
                source_path=source_path,
                target_dir=target_dir
            )
            self.assertEqual(self.helper.status, StepHelper.Status.FINISH)


class TestWorker(unittest.TestCase):

    def setUp(self):
        db.init()
        self.tmp_dir = tempfile.TemporaryDirectory()
        gen_struct(self.tmp_dir.name)

        self.q = queue.Queue()
        self.event = threading.Event()
        self.worker = Worker(self.q, 1, self.event)

    def tearDown(self) -> None:
        self.event.set()
        self.tmp_dir.cleanup()
        os.remove("s7.db")

    def test_worker_runs(self):
        self.worker.start()
        self.assertTrue(self.worker.is_alive())

    def test_worker_stops(self):
        self.worker.start()
        self.event.set()
        self.worker.join()
        self.assertFalse(self.worker.is_alive())

    def test_worker_processes_files(self):
        name = "20221129_1234_DME.csv"
        file = f"{self.tmp_dir.name}/in/{name}"

        data_file = """num;surname;firstname;bdate\n1;IVANOV;IVAN;11NOV73\n2;PETROV;ALEXANDER;13JUL79\n3;BOSHIROV;RUSLAN;12APR78"""
        with open(file, "w") as f:
            f.write(data_file)

        self.q.put(file)
        self.worker.start()

        ok_dir = f"{self.tmp_dir.name}/ok"
        err_dir = f"{self.tmp_dir.name}/err"
        out_dir = f"{self.tmp_dir.name}/out"

        time.sleep(2)
        files = file_handler.list_files(err_dir, extension=".csv")
        self.assertEqual(len(files), 0)
        files = file_handler.list_files(ok_dir, extension=".csv")
        self.assertIn(f"{ok_dir}/{name}", files)
        files = file_handler.list_files(out_dir, extension=".json")
        self.assertIn(f"{out_dir}/{name[:-3] + 'json'}", files)
