import logging
import socket

from base_process import BaseProcess

logger = logging.getLogger("WebProcess")


class WebProcess(BaseProcess):
    count_worker = 1

    def __init__(self, socker: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.host, self.port = socker.split(":")

    def run(self) -> None:
        from .server import app
        import asyncio
        from hypercorn.config import Config
        from hypercorn.asyncio import serve
        cf = Config()
        cf.accesslog = logger
        asyncio.run(serve(app, cf))

    def test(self) -> bool:
        s = socket.socket()
        is_good = True
        try:
            s.connect((self.host, self.port))
        except Exception as e:
            logger.error("something's wrong with %s:%d. Exception is %s" % (self.host, self.port, e))
            is_good = False
        finally:
            s.close()
            return is_good
