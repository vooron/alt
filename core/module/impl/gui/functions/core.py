from typing import Dict, Callable, Optional

from core.application.function import Function, CommandResponse
from core.module.impl.gui.connection import UiCommunicationSignal


class CoreFunction(Function):

    _signal: UiCommunicationSignal

    def __init__(self, signal: UiCommunicationSignal):
        super().__init__()
        self._signal = signal

    def _init_commands(self) -> Dict[str, Callable[[dict, dict], Optional[CommandResponse]]]:
        pass

    def wake_up(self, payload: dict, context: dict) -> Optional[CommandResponse]:
        pass

    def close(self, payload: dict, context: dict) -> Optional[CommandResponse]:
        pass
