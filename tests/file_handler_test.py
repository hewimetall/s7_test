import os
import shutil
import tempfile
import unittest

from file_handler import create_directory, move_file, list_files, delete_file


class TestFileHandler(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_create_directory(self):
        new_dir = os.path.join(self.tmp_dir, 'new_dir')
        create_directory(new_dir)
        self.assertTrue(os.path.isdir(new_dir))

        create_directory(new_dir)
        self.assertTrue(os.path.isdir(new_dir))

    def test_move_file(self):
        source_file = os.path.join(self.tmp_dir, 'source.txt')
        with open(source_file, 'w') as f:
            f.write('test')

        target_dir = os.path.join(self.tmp_dir, 'target')
        move_file(source_file, target_dir)
        self.assertTrue(os.path.isdir(target_dir))
        self.assertFalse(os.path.isfile(source_file))
        self.assertTrue(os.path.isfile(os.path.join(target_dir, 'source.txt')))

        move_file(os.path.join(target_dir, 'source.txt'), target_dir)
        self.assertTrue(os.path.isdir(target_dir))
        self.assertTrue(os.path.isfile(os.path.join(target_dir, 'source.txt')))

    def test_list_files(self):
        file1 = os.path.join(self.tmp_dir, 'file1.txt')
        file2 = os.path.join(self.tmp_dir, 'file2.txt')
        with open(file1, 'w') as f:
            f.write('test')
        with open(file2, 'w') as f:
            f.write('test')

        files = list_files(self.tmp_dir)
        self.assertListEqual(files, [file2, file1, ])

        files = list_files(self.tmp_dir, extension='.txt')
        self.assertListEqual(files, [file2, file1])

        files = list_files(self.tmp_dir, extension='.csv')
        self.assertListEqual(files, [])

    def test_delete_file(self):
        file_to_delete = os.path.join(self.tmp_dir, 'file.txt')
        with open(file_to_delete, 'w') as f:
            f.write('test')

        delete_file(file_to_delete)
        self.assertFalse(os.path.isfile(file_to_delete))
