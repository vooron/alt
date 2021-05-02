from abc import abstractmethod, ABCMeta

from core.application.application import Application
from core.communication.command_identifier import ApplicationType
from core.communication.connection_service import ConnectionService


class Module(Application, metaclass=ABCMeta):

    def __init__(self, id: str):
        super().__init__(id, ApplicationType.MODULE)

    @abstractmethod
    def setup(self, connection_service: ConnectionService) -> None:
        pass
