from typing import Dict, Callable, Optional

from core.application.function import Function, CommandResponse
from core.communication.callback import Callback
from core.communication.command_identifier import CommandIdentifier


class UserQueryProcessingFunction(Function):

    def _init_commands(self) -> Dict[str, Callable[[dict, dict, Optional[Callback]], Optional[CommandResponse]]]:
        pass

    def _resolve_data(self, key: str, payload: dict, context: dict):
        if key in payload:
            return payload[key]


    def _resolve_command(self, payload: dict, context: dict, callback: Optional[Callback]) -> Optional[CommandResponse]:
        """Main"""
        pass



