import logging
from queue import Queue

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer as WatchdogObserver

import file_handler
import settings
from schema import FlightFromName

logger = logging.getLogger("Watcher:")


class MyHandler(FileSystemEventHandler):
    ext = '.csv'

    def __init__(self, q: Queue):
        self.q = q

    def notif(self, src_path: str):
        if self.q.full():
            logger.critical(f"Full Queue\n \t file not load {src_path}.")
        else:
            self.q.put_nowait(src_path)

    def check(self, file_path: str) -> bool:
        try:
            FlightFromName.to_python(file_path)
            return True
        except Exception as e:
            file_handler.move_file(
                source_path=file_path,
                target_dir=settings.PATH + "/err"
            )
            logger.error(f"Convert err:\n {str(e)}")
            return False

    def on_created(self, event):
        src_path = getattr(event, 'src_path')

        if src_path[-4:] == self.ext and self.check(src_path):
            self.notif(src_path)
        else:
            logger.warning(f"Not correct filename {src_path}")


class Observer(WatchdogObserver):

    def __init__(self, q: Queue, path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schedule(MyHandler(q),
                      path=path,
                      recursive=False)
