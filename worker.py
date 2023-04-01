import enum
from threading import Thread
from queue import Queue
import logging
from csv_to_json import csv_to_json
import utils

logger = logging.getLogger("Workers")

class StepHelper(object):
    class Status(enum.Enum):
        INIT = None
        FAIL = 0
        SUCCESS = 1
        FINISH = 2


    def __init__(self, filename):
        self.filename = filename
        self.status = self.Status.INIT

    def get_status(self):
        return self._status

    def set_status(self, val):
        self._status = self.Status(val)

    status = property(
        fget=get_status,
        fset=set_status,
    )

    def start(self):
        """ Создает файл и запист в базе. """
        status = csv_to_json(self.filename)
        status += utils.parsing_to_db(self.filename)
        self.status = status

    def fail(self):
        """ Процесс отката условий
                Копирует файл в err
        """
        self.status = self.Status.FINISH

    def success(self):
        """ Копирует файл в директорию ok """

class Worker(Thread):
    def __init__(self, q:Queue, number:int):
        Thread.__init__(self)
        self.q = q
        self.number = number


    def run(self):
        logging.debug(f"START Thread {self.number}")
        while True:
            file = self.q.get(block=True)
            logger.debug(f"Thread_{self.number} GET FILE {file}")
            helper = StepHelper(file)
            helper.start()
            if helper.status:
                logger.error(f"File {file} process fail.")
                helper.fail()
            else:
                helper.success()
