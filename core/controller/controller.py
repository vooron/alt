import logging
from typing import Dict, List, Callable

from core.application.application import Application
from core.communication.command_identifier import ApplicationType, CommandIdentifier
from core.communication.connection_service import ConnectionService
from core.communication.message import Message
from core.module.module import Module


class Controller:
    _modules: Dict[str, Module]
    _applications: Dict[str, Application]
    _connection_service: ConnectionService

    _cycle_handlers: List[Callable[[], None]]

    def __init__(self, modules: Dict[str, Module], applications: Dict[str, Application]):
        self._modules = modules
        self._connection_service = ConnectionService(self.on_event)
        self._applications = applications
        self._cycle_handlers = []

    def on_event(self, event: Message):
        """check access permissions, translate event to target or handler"""
        logging.info(f"Event from {event.source} accepted by controller")
        self._connection_service.dispatch(event)

    def _setup_modules(self):
        logging.info("=== Init modules start ===")
        for module_name, module in self._modules.items():
            module.setup(self._connection_service)
            module.register_cycle_handlers(lambda handler: self._cycle_handlers.append(handler))
            logging.info(f"Module {module_name} inited.")
        logging.info("=== Init modules end ===")

    def _setup_applications(self):
        logging.info("=== Init applications start ===")
        for application_name, application in self._applications.items():
            application.setup(self._connection_service)
            logging.info(f"Application {application_name} inited.")
        logging.info("=== Init applications end ===")

    def _start_event_loop(self):
        while True:
            for handle in self._cycle_handlers:
                handle()

    def setup(self) -> None:

        self._setup_modules()
        self._setup_applications()

        self._connection_service.dispatch(Message(
            payload={},
            target=CommandIdentifier(
                ApplicationType.MODULE, "UI", "core", "wakeUp"
            ),
            source=None,
            context={}
        ))

        self._start_event_loop()
