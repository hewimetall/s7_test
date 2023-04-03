from enum import Enum, auto

DATABASE = "s7.db"
SOCKET = "localhost:8000"
PATH = "/home/xx/PycharmProjects/s7_test/test"


class ExistCode(int, Enum):
    BD_EXIST = auto()
    TEST_PROCESS = auto()
    START_PROCESS = auto()
