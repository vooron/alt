from abc import ABCMeta, abstractmethod
from typing import Dict, Callable, Optional, NamedTuple

from core.application.exceptions import CommandNotFound
from core.communication.callback import Callback
from core.communication.command_identifier import CommandIdentifier

dispatch_event_function_type = Callable[[dict, CommandIdentifier, Optional[Callback]], None]


class CommandResponse(NamedTuple):
    payload: dict
    context: dict
    target: CommandIdentifier
    callback: Optional[Callback]


class Function(metaclass=ABCMeta):
    """
    Some functionality that can be executed.
    Like SkillFunction(switch on the lamp) or CoreFunction(text to function execution)
    ---
    Accept event from the Application and resolve each command to execute. Controls lifecycle.
    To each flow should be provided an ability to dispatch event to another function (with callback if needed).
    """

    _commands: Dict[str, Callable[[dict, dict, Optional[Callback]], Optional[CommandResponse]]]

    def __init__(self):
        self._commands = self._init_commands()

    @abstractmethod
    def _init_commands(self) -> Dict[str, Callable[[dict, dict], Optional[CommandResponse]]]:
        pass

    def execute(
            self,
            command_id: str,
            payload: dict,
            context: dict,
            callback: Optional[Callback],
            dispatch_event_function: Callable[[dict, dict, CommandIdentifier, Optional[Callback]], None]
    ) -> None:
        if command_id not in self._commands:
            raise CommandNotFound("No such command in the system")

        response = self._commands[command_id](payload, context, callback)

        if response:
            dispatch_event_function(response.payload, response.context, response.target, response.callback)

