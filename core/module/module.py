from abc import abstractmethod, ABCMeta

from core.communication.event import Event


class Module(metaclass=ABCMeta):

    @property
    @abstractmethod
    def is_online(self) -> bool:
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def emit(self, event: Event):
        pass
