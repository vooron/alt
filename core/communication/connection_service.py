import logging
from typing import Dict, Callable

from core.communication.command_identifier import ApplicationType
from core.communication.connection import Connection
from core.communication.message import Message


class ConnectionService:
    # TODO: add different connection integrations, like WebsocketServer
    _connections: Dict[ApplicationType, Dict[str, Connection]]
    _on_event: Callable[[Message], None]

    def __init__(self, on_event: Callable[[Message], None]):
        self._on_event = on_event
        self._connections = {
            ApplicationType.MODULE: {},
            ApplicationType.CORE: {},
            ApplicationType.SKILL: {}
        }

    def add_connection(self, application_type: ApplicationType, application: str, connection: Connection):
        # TODO: check this application type can be added, etc
        # TODO: add checks that connection available, valid, authenticated and not already exists.
        self._connections[application_type][application] = connection

        connection.set_on_close(lambda: self.on_close_connection(application_type, application, connection))
        connection.set_on_message(lambda message: self.on_message(application_type, application, message))
        logging.info(f"Connection {application_type}.{application} was added.")

    def on_close_connection(self, application_type: ApplicationType, application: str, connection: Connection):
        del self._connections[application_type][application]
        logging.info(f"Connection {application_type}.{application} was closed.")

    def on_message(self, application_type: ApplicationType, application: str, message: str):
        logging.info(f"Message from {application_type}.{application}")
        event = Message.deserialize(message)

        if event.source.type != application_type or event.source.application != application:
            raise ConnectionAbortedError(f"Event with fake source: real {application_type}.{application},"
                                         f" received {event.source.type}.{event.source.application}")

        self._on_event(event)

    def dispatch(self, event: Message):
        logging.info(f"Send event from {event.source} to {event.target}")

        if event.target.application not in self._connections[event.target.type]:
            logging.error(f"No such topic {event.target} in the system")
            return

        if not self._connections[event.target.type][event.target.application].is_connected:
            logging.error(f"Connection is not connected.")
            return

        self._connections[event.target.type][event.target.application].dispatch(event)
