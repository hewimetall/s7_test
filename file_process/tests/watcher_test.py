import logging
import unittest
from queue import Queue
from unittest.mock import MagicMock, patch

from file_process.watcher import MyHandler


class WatherTest(unittest.TestCase):
    def test_check_valid_file(self):
        handler = MyHandler(Queue())
        valid_file = 'path/to/valid_file.csv'
        with patch("schema.FlightFromName.to_python", return_value=True):
            self.assertTrue(handler.check(valid_file))

    def test_check_invalid_file(self):
        handler = MyHandler(Queue())
        invalid_file = 'path/to/invalid_file.csv'
        with patch("schema.FlightFromName.to_python", side_effect=Exception('Invalid File')):
            with patch("file_handler.move_file"):
                self.assertFalse(handler.check(invalid_file))

    def test_notif_queue_full(self):
        handler = MyHandler(Queue(maxsize=1))
        handler.q.put_nowait('path/to/file1.csv')
        logger = logging.getLogger('Watcher:')
        logger.critical = MagicMock()
        handler.notif('path/to/file2.csv')
        logger.critical.assert_called_with('Full Queue\n \t file not load path/to/file2.csv.')

    def test_notif_queue_not_full(self):
        handler = MyHandler(Queue(maxsize=2))
        handler.q.put_nowait('path/to/file1.csv')
        logger = logging.getLogger('Watcher:')
        logger.critical = MagicMock()
        handler.notif('path/to/file2.csv')
        handler.notif('path/to/file3.csv')
        self.assertEqual(logger.critical.call_count, 1)

    def test_on_created_with_valid_file(self):
        handler = MyHandler(Queue())
        handler.check = MagicMock(return_value=True)
        handler.notif = MagicMock()
        logger = logging.getLogger('Watcher:')
        logger.warning = MagicMock()
        event = MagicMock()
        event.src_path = 'path/to/valid_file.csv'
        handler.on_created(event)
        handler.check.assert_called_with('path/to/valid_file.csv')
        handler.notif.assert_called_with('path/to/valid_file.csv')
        logger.warning.assert_not_called()

    def test_on_created_with_invalid_file(self):
        handler = MyHandler(Queue())
        handler.check = MagicMock(return_value=False)
        handler.notif = MagicMock()
        logger = logging.getLogger('Watcher:')
        logger.warning = MagicMock()
        event = MagicMock()
        event.src_path = 'path/to/invalid_file.csv'
        handler.on_created(event)
        handler.check.assert_called_with('path/to/invalid_file.csv')
        handler.notif.assert_not_called()
        logger.warning.assert_called_with('Not correct filename path/to/invalid_file.csv')
