import os
import tempfile
import time
import unittest

import db
import file_handler
from file_process import FileProcess


def gen_struct(tmp):
    dirs = [
        "in",
        "out",
        "ok",
        "err"
    ]
    for dir in dirs:
        file_handler.create_directory(f"{tmp}/{dir}")


class TestFileProcess(unittest.TestCase):

    def setUp(self):
        db.init()
        self.tmp_dir = tempfile.TemporaryDirectory()
        gen_struct(self.tmp_dir.name)
        self.fileprocess = FileProcess(self.tmp_dir.name)

    def tearDown(self):
        self.tmp_dir.cleanup()
        os.remove("s7.db")

    def test_run(self):
        self.fileprocess.run()
        name = "20221129_1234_DME.csv"
        file = f"{self.tmp_dir.name}/in/{name}"

        data_file = """num;surname;firstname;bdate\n1;IVANOV;IVAN;11NOV73\n2;PETROV;ALEXANDER;13JUL79\n3;BOSHIROV;RUSLAN;12APR78"""
        with open(file, "w") as f:
            f.write(data_file)
        time.sleep(15)
        ok_dir = f"{self.tmp_dir.name}/ok"
        err_dir = f"{self.tmp_dir.name}/err"
        out_dir = f"{self.tmp_dir.name}/out"

        files = file_handler.list_files(err_dir, extension=".csv")
        self.assertEqual(len(files), 0)
        files = file_handler.list_files(ok_dir, extension=".csv")
        self.assertIn(f"{ok_dir}/{name}", files)
        files = file_handler.list_files(out_dir, extension=".json")
        self.assertIn(f"{out_dir}/{name[:-3] + 'json'}", files)

        self.fileprocess.stop_worker()

    def test_test(self):
        result = self.fileprocess.test()
        self.assertTrue(result)
