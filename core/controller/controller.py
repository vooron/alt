import logging
from typing import Dict, Callable

from core.communication.callback import Callback
from core.communication.connection_service import ConnectionService
from core.communication.message import Message
from core.communication.command_identifier import CommandIdentifier, ApplicationType
from core.module.module import Module


class Controller:

    _subscriptions: Dict[CommandIdentifier, Callable[[Message], None]]
    _modules: Dict[str, Module]
    _connection_service: ConnectionService

    def __init__(self, subscriptions: Dict[CommandIdentifier, Callable[[Message], None]], modules: Dict[str, Module]):
        self._modules = modules
        self._subscriptions = subscriptions
        self._connection_service = ConnectionService(self.on_event)

    def on_event(self, event: Message):
        """check access permissions, translate event to target or handler"""
        print(event)

    def _setup_modules(self):
        logging.info("=== Init modules start ===")
        for module_name, module in self._modules.items():
            module.setup(self._connection_service)
            logging.info(f"Module {module_name} inited.")
        logging.info("=== Init modules end ===")

    def setup(self) -> None:
        self._setup_modules()

        self._connection_service.dispatch(Message(
            source=None,
            target=CommandIdentifier(ApplicationType.MODULE, "TextIndexer", "indexation", "get_indexed_data"),
            context={},
            callback=Callback(target=CommandIdentifier(ApplicationType.CORE, "app", "function", "command")),
            payload={
                "test": {
                    "type": "SKILL",
                    "name": "Test",
                    "description": "Some text",
                    "tags": ["Test", "Test1"]
                },
                "test.function": {
                    "type": "SKILL_FUNCTION",
                    "name": "Test",
                    "description": "Some text",
                    "call_examples": ["Test", "Test1"]
                },
            }
        ))

