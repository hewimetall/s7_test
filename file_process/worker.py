import enum
import logging
import pathlib
import threading
import time
from queue import Queue
from threading import Thread

import db
import file_handler
import file_process.utils as utils
from schema import FlightFromName, PathHelper

logger = logging.getLogger("Workers")


class StepHelper(object):
    class Status(str, enum.Enum):
        FAIL = 0
        SUCCESS = 1
        FINISH = 2

    def __init__(self, file_path: str):
        self.file_path = PathHelper.to_python(file_path)
        try:
            self.flight = FlightFromName.to_python(file_path)
            self.status = None
        except:
            self.status = self.Status.FAIL

    def start(self):
        """ Создает файл и запись в базе. """
        try:
            if all(map(
                    lambda f: f(self.flight),
                    [utils.parsint_to_file, utils.parsing_to_db]
            )):
                self.status = self.Status.SUCCESS
            else:
                self.status = self.Status.FAIL
        except Exception as e:
            logger.error(f"ERR:{e}")
            self.status = self.Status.FAIL

    def fail(self):
        """ Откатывает sucsess и переместить файл в каталог с ошибкой """
        if self.flight is not None:
            cn = db.get_db()
            db.delete_row(cn, self.flight.filename, date=self.flight.date)
            cn.close()
            try:
                file_handler.delete_file(self.flight.file_path.path_out())
            except:
                pass
        file_handler.move_file(
            source_path=str(self.flight.file_path),
            target_dir=str(self.flight.file_path.path_err())
        )
        self.status = self.Status.FINISH

    def success(self):
        """ Перемещяет файл в директорию ok """
        file_handler.move_file(
            source_path=str(self.flight.file_path),
            target_dir=str(self.flight.file_path.path_ok())
        )
        self.status = self.Status.FINISH

class Worker(Thread):
    def __init__(self, q: Queue, number: int, event: threading.Event, *args, **kwargs):
        Thread.__init__(self, *args, **kwargs)
        self.q = q
        self.number = number
        self.event = event

    def run(self):
        logging.info(f"START Worker Process {self.number}")
        while not self.event.is_set():
            if not self.q.empty():
                file = self.q.get(block=False)
                logger.debug(f"Thread_{self.number} GET FILE {file}")
                helper = StepHelper(file)
                if helper.status == None:
                    helper.start()

                if helper.status:
                    helper.success()
                else:
                    logger.error(f"File {file} process fail.")
                    helper.fail()

            else:
                time.sleep(self.number)
