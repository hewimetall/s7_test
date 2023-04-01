import time
from watchdog.observers import Observer as WatchdogObserver
from watchdog.observers.polling import PollingObserver
from watchdog.events import PatternMatchingEventHandler
import logging

class MyHandler(PatternMatchingEventHandler):
    _patterns = "*.csv"

    def on_created(self, event):
        if event.is_directory:
            print(f"Directory created:{event.src_path}")
        else:
            print(f"File created:{event.src_path}")

class Observer(WatchdogObserver):
    def __init__(self):
        if issubclass(self, PollingObserver):
            logging.warning("Система не поддержвает механизм наблюдения за событиями.")
        self.event_handler = PatternMatchingEventHandler(
            "*.csv"
        )
        self.event_handler.on_created()


if __name__ == "__main__":
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path='./test', recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
