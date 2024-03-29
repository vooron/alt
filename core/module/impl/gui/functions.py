from typing import Dict, Callable, Optional

from core.application.function import Function, CommandResponse
from core.communication.callback import Callback
from core.module.impl.gui.connection import UiCommunicationSignal, CommandMessage


class CoreFunction(Function):
    _signal: UiCommunicationSignal

    def __init__(self, signal: UiCommunicationSignal):
        super().__init__()
        self._signal = signal

    def _init_commands(self) -> Dict[str, Callable[[dict, dict, Optional[Callback]], Optional[CommandResponse]]]:
        return {
            "wakeUp": self.wake_up,
            "hide": self.hide,
            "askUserSelectCommandFromVariants": self.ask_user_select_command_from_variants
        }

    def wake_up(self, payload: dict, context: dict, callback: Optional[Callback]) -> Optional[CommandResponse]:
        self._signal.ui_input.emit(
            CommandMessage(topic="add_card", payload={
                "card_type": "MainCard",
                "params": dict()
            }).serialize()
        )

        return

    def ask_user_select_command_from_variants(
            self, payload: dict, context: dict, callback: Optional[Callback]
    ) -> Optional[CommandResponse]:
        self._signal.ui_input.emit(CommandMessage(
            topic="add_card",
            payload={
                "card_type": "ListCard",
                "params": {
                    "items": [{
                        "label": i['label']
                    } for i in payload['variants']]
                }
            }
        ).serialize())
        return

    def hide(self, payload: dict, context: dict, callback: Optional[Callback]) -> Optional[CommandResponse]:
        self._signal.ui_input.emit(
            CommandMessage(topic="hide_interface", payload={}).serialize()
        )
        return
