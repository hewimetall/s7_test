from queue import Queue
from watchdog.observers import Observer as WatchdogObserver
from watchdog.events import FileSystemEventHandler
import logging

from schema import FlightFromDB

logger = logging.getLogger("Watcher:")

class MyHandler(FileSystemEventHandler):
    ext = '.csv'

    def __init__(self, q:Queue):
        self.q = q

    def notif(self, src_path:str):
        if self.q.full():
            logger.critical(f"Full Queue\n \t file not load {src_path}.")
        else:
            self.q.put_nowait(src_path)

    def check(self, file_path:str)->bool:
        try:
            FlightFromDB.to_python(file_path)
            return True
        except Exception as e:
            logger.error(f"Convert err:\n {e.__traceback__}")
            return False
    def on_created(self, event):
        src_path = getattr(event, 'src_path')

        if  src_path[-4:] == self.ext and self.check(src_path):
            self.notif(src_path)
        else:
            logger.warning(f"Not correct filename {src_path}")

class Observer(WatchdogObserver):

    def __init__(self, q:Queue, path:str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schedule(MyHandler(q),
                          path=path,
                          recursive=False)
