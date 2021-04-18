import sys
import threading

from PySide2.QtWidgets import QApplication

from core.communication.callback import Callback
from core.communication.event import Event
from core.communication.topic import Topic
from core.module.impl.gui.main_window import MainWindow
from core.module.module import Module


class UIModule(Module):
    MODULE_ID = "FrontEnd"
    # TODO: should have a link to a connections server and setup Websocket or local connection

    _is_launched: bool = False
    _main_window: MainWindow

    @property
    def is_online(self) -> bool:
        return self._is_launched

    def _setup(self):
        app = QApplication(sys.argv)
        self._main_window = MainWindow(self._emit_event)
        sys.exit(app.exec_())

    def setup(self):
        ui_thread = threading.Thread(target=self._setup)
        ui_thread.start()
        self._is_launched = True

    def _emit_event(self, payload: dict, topic: Topic, session_id: str, callback: Callback = None):
        # TODO: create class for sync and/or async communication between local modules and core.
        # TODO: try connect controller to signal
        pass

    async def emit(self, event: Event):
        self._main_window.controller_message_signal.emit(event.serialize())
