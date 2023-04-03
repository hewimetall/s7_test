import logging
import pathlib
import threading
from multiprocessing import Process
from queue import Queue

from file_handler import list_files
from file_process.utils import test_dirs
from file_process.watcher import Observer
from file_process.worker import Worker

logger = logging.getLogger("FileProcess")


class FileProcess(Process):
    max_worker = 5

    def __init__(self, path: str, *args, **kwargs):
        self.path = pathlib.Path(path)
        super().__init__(*args, **kwargs)

    def stop_worker(self):
        self.event.set()
        self.observer.stop()

    def run(self):
        self.event = threading.Event()
        self.worker = []
        q = Queue()
        for item in list_files(self.path.joinpath("in"), extension="csv"):
            q.put(item)

        self.observer = Observer(q, self.path.joinpath("in").__str__())
        self.workers = [Worker(q, i + 1, self.event, daemon=False) for i in range(self.max_worker)]
        self.workers.append(self.observer)
        for th in self.workers:
            th.start()
        logging.info(f"START WORKERS {'.' * self.max_worker}")

    def test(self) -> bool:
        list_dirs = [
            "in",
            "out",
            "err",
            "ok"
        ]

        try:
            return all(map(lambda dirs: test_dirs(self.path.joinpath(dirs)), list_dirs))
        except Exception as e:
            logger.error(e)
            return False
