import logging
import sys

import db
import settings
from file_handler import gen_struct
from file_process import FileProcess
from web_process import WebProcess

logging.basicConfig(filename='service.log', level=logging.INFO)
logger = logging.getLogger("Main:")

def main():
    gen_struct(settings.PATH)
    if db.init():
        logger.info("Ok db")
    else:
        logger.critical("DB is fail")
        sys.exit(settings.ExistCode.BD_EXIST)

    process = [FileProcess(settings.PATH, daemon=False),
               WebProcess(settings.SOCKET, daemon=False)]

    if all(map(lambda pr: pr.test(), process)):
        logger.info(f"Ok process test{'.' * len(process)}")
    else:
        logger.critical(f"Process test fail.")
        sys.exit(settings.ExistCode.TEST_PROCESS)

    try:
        for pr in process:
            pr.start()
    except Exception as e:
        logger.critical(f"Process run fail. {e}")
        sys.exit(settings.ExistCode.START_PROCESS)
    else:
        logger.info(f"Ok process start{'.' * len(process)}")

if __name__ == '__main__':
    main()