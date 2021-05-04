from abc import abstractmethod, ABCMeta
from typing import Callable

from core.application.application import Application
from core.communication.command_identifier import ApplicationType


class Module(Application, metaclass=ABCMeta):

    def __init__(self, id: str):
        super().__init__(id, ApplicationType.MODULE)

    @abstractmethod
    def register_cycle_handlers(self, register_cycle_handler: Callable[[Callable[[], None]], None]):
        """Adds all function that should be executed on each cycle of event loop"""
        pass
