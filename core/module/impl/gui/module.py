import sys
import threading
from typing import Dict

from PySide2.QtWidgets import QApplication

from core.application.function import Function
from core.communication.command_identifier import ApplicationType
from core.communication.connection import SyncConnection
from core.communication.connection_service import ConnectionService
from core.module.impl.gui.connection import UiCommunicationSignal
from core.module.impl.gui.main_window import MainWindow
from core.module.module import Module


class UIModule(Module):
    _main_window: MainWindow
    _signal: UiCommunicationSignal

    def _setup(self):
        app = QApplication(sys.argv)
        self._signal = UiCommunicationSignal()

        self._main_window = MainWindow(self._signal)
        sys.exit(app.exec_())

    def _init_functions(self) -> Dict[str, Function]:
        pass

    def setup(self, connection_service: ConnectionService):
        ui_thread = threading.Thread(target=self._setup)
        ui_thread.start()

        connection = SyncConnection(self._on_event)

        connection_service.add_connection(ApplicationType.MODULE, self.id, connection)
