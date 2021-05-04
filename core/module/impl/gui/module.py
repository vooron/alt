import json
import sys
from typing import Dict, Callable

from PySide2.QtWidgets import QApplication

from core.application.function import Function
from core.communication.command_identifier import ApplicationType, CommandIdentifier
from core.communication.connection import SyncConnection
from core.communication.connection_service import ConnectionService
from core.communication.message import Message
from core.module.impl.gui.connection import UiCommunicationSignal
from core.module.impl.gui.functions import CoreFunction
from core.module.impl.gui.main_window import MainWindow
from core.module.module import Module


class UIModule(Module):
    _main_window: MainWindow
    _signal: UiCommunicationSignal
    _app: QApplication

    _events_handler: Dict[str, Callable[[dict], None]]

    def __init__(self, id: str):
        self._signal = UiCommunicationSignal()
        super().__init__(id)

        self._signal.ui_output.connect(self._on_event_from_UI)

        self._events_handler = {
            "userQueryEntered": self._user_query_entered
        }

    def _user_query_entered(self, payload: dict):
        self._connection.send_message(Message(
            payload=payload,
            target=CommandIdentifier(ApplicationType.CORE, "UserQueryProcessing", "processUserQueryFunction", "main"),
            source=CommandIdentifier(self.application_type, self.id),
            context={}
        ).serialize())

    def _init_functions(self) -> Dict[str, Function]:
        return {
            "core": CoreFunction(self._signal)
        }

    def _on_event_from_UI(self, message: str):
        data = json.loads(message)
        self._events_handler[data['topic']](data['payload'])

    def register_cycle_handlers(self, register_cycle_handler: Callable[[Callable[[], None]], None]):
        register_cycle_handler(lambda: self._app.processEvents())

    def setup(self, connection_service: ConnectionService):
        self._app = QApplication(sys.argv)
        self._main_window = MainWindow(self._signal)
        self._connection = SyncConnection(self._on_event)

        connection_service.add_connection(ApplicationType.MODULE, self.id, self._connection)
