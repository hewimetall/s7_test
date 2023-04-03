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

    def process(self, path: str):
        if path[-4:] == self.ext and self.check(path):
            self.notif(path)
        else:
            logger.warning(f"Not correct filename {path}")

    def on_created(self, event):
        src_path = getattr(event, 'src_path', None)
        if src_path:
            self.process(src_path)

    def on_moved(self, event):
        dest_path = getattr(event, 'dest_path', None)
        src_path: str = getattr(event, 'src_path', None)
        if src_path.endswith("_init"):
            self.process(dest_path)
        else:
            logger.warning(f"File moved {src_path}->{dest_path}")


class Observer(WatchdogObserver):

    def __init__(self, q: Queue, path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.schedule(MyHandler(q),
                      path=path,
                      recursive=False)

