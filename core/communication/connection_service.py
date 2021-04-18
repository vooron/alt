import logging
from typing import Dict, Callable

from core.communication.connection import Connection
from core.communication.event import Event
from core.communication.topic import Topic


class ConnectionService:

    # TODO: add different connection integrations, like WebsocketServer
    _connections: Dict[Topic, Connection]

    _on_event: Callable[[Event], None]

    def __init__(self, on_event: Callable[[Event], None]):
        self._on_event = on_event

    def on_add_connection(self, topic: Topic, connection: Connection):
        # TODO: add checks that connection available, valid, authenticated and not already exists.
        self._connections[topic] = connection
        connection.set_on_close(lambda: self.on_close_connection(topic, connection))
        logging.info(f"Connection {topic}|{connection} was added.")

    def on_close_connection(self, topic: Topic, connection: Connection):
        del self._connections[topic]
        logging.info(f"Connection {topic}|{connection} was closed.")
