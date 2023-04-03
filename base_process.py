import abc
from multiprocessing import Process


class BaseProcess(Process):
    @abc.abstractmethod
    def run(self):
        """"""

    @abc.abstractmethod
    def test(self) -> bool:
        """"""
