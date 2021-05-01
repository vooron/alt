from abc import abstractmethod, ABCMeta

from core.application.application import Application
from core.communication.connection_service import ConnectionService


class Module(Application, metaclass=ABCMeta):

    @abstractmethod
    def setup(self, connection_service: ConnectionService) -> None:
        pass
