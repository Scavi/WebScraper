import abc
from abc import ABC


class AbstractNotification(ABC):
    @abc.abstractmethod
    def notify(self) -> None:
        pass
