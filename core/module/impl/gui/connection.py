import dataclasses
import json
from dataclasses import dataclass
from typing import Callable

from PySide2.QtCore import QObject, Signal

from core.communication.connection import Connection
from core.communication.message import Message


class UiCommunicationSignal(QObject):
    # https://stackoverflow.com/questions/36453462/pyqt5-qobject-cannot-create-children-for-a-parent-that-is-in-a-different-thread
    ui_input = Signal(str)
    ui_output = Signal(str)


@dataclass
class CommandMessage:
    topic: str
    payload: dict

    def serialize(self) -> str:
        return json.dumps(dataclasses.asdict(self))


class QtSignalConnection(Connection):
    _signal_wrapper: UiCommunicationSignal

    def __init__(self, signal_wrapper: UiCommunicationSignal):
        self._signal_wrapper = signal_wrapper

    def set_on_message(self, on_message: Callable[[str], None]):
        if self._on_message:
            self._signal_wrapper.ui_output.disconnect(self._on_message)
        self._signal_wrapper.ui_output.connect(on_message)
        super(QtSignalConnection, self).set_on_message(on_message)

    async def dispatch(self, event: Message) -> None:
        self._signal_wrapper.ui_input.emit(event.serialize())  # noqa

    async def connect(self) -> None:
        return

    async def _close(self) -> None:
        return

    @property
    async def is_connected(self) -> bool:
        return True
