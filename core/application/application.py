import logging
from abc import ABCMeta, abstractmethod
from typing import Dict, Optional

from core.application.exceptions import CommandNotFound
from core.application.function import Function
from core.communication.callback import Callback
from core.communication.command_identifier import CommandIdentifier, ApplicationType
from core.communication.connection import Connection
from core.communication.connection_service import ConnectionService
from core.communication.message import Message

from core.communication.context_scope import ContextScope


class Application(metaclass=ABCMeta):
    """
    A group of functions, related to the same application, functionality, or etc.
    ---
    Accepts events from connection service, resolve which functions should be called.
    """
    _connection: Connection
    _functions: Dict[str, Function]

    application_type: ApplicationType
    id: str

    def __init__(self, id: str, application_type: ApplicationType):
        self.id = id
        self.application_type = application_type
        self._functions = self._init_functions()

    @abstractmethod
    def _init_functions(self) -> Dict[str, Function]:
        pass

    @abstractmethod
    def setup(self, connection_service: ConnectionService):
        """Should prepare application and establish connection"""
        pass

    def _dispatch_event(
            self,
            function_id: str,
            command_id: str,
            payload: dict,
            context: dict,
            target: CommandIdentifier,
            callback: Optional[Callback]
    ) -> None:
        self._connection.send_message(Message(
            payload=payload,
            target=target,
            source=CommandIdentifier(
                type=self.application_type, application=self.id, function=function_id, command=command_id
            ),
            context=context,
            callback=callback
        ).serialize())

    def _on_event(self, event: Message):
        if event.target.function not in self._functions:
            logging.error(f"No such function({event.target.function}) in the system.")
            return

        context_scope = ContextScope(application=self.id, function=event.target.function)
        context = event.context.get(context_scope)
        if context is None:
            context = {}

        try:
            self._functions[event.target.function].execute(
                event.target.command,
                event.payload,
                context,
                event.callback,
                lambda payload, context, target, callback: self._dispatch_event(
                    event.target.function,
                    event.target.command,
                    payload,
                    {
                        **event.context,  # IMPORTANT: context for the same command can be overwritten
                        context_scope: context
                    },
                    target,
                    callback
                )
            )
        except CommandNotFound:
            logging.error(f"No such command {event.target.command} in function {event.target.function}.")
            return
