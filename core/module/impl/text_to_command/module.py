from typing import Dict, Callable

from core.communication.connection import Connection, SyncConnection
from core.communication.connection_service import ConnectionService
from core.communication.event import Message
from core.module.module import Module


class TextToCommandModule(Module):
    MODULE_ID = "TextToCommand"

    _is_launched: bool = False

    _events_mapping: Dict[str, Callable[[Message], None]]
    _connection: Connection

    def __init__(self):
        self._events_mapping = {
            "GetEmbedding": self._get_embeddings
        }

    def _on_input_event(self, event: Message):
        handler = self._events_mapping.get(event.target.id)
        if not handler:
            self._response_back(event, dict(
                code=404,  # TODO: add error codes
                detail="No such route in the system"
            ))
            return
        handler(event)

    def _response_back(self, event: Message, payload: dict):
        if event.callback:
            self._on_message(Message(
                payload=payload,
                topic=event.callback.target
            ))

    # --- Actions -------------------------
    def _get_embeddings(self, event: Message):
        query_embedding = event.payload.get("query_embedding")
        if not query_embedding:
            self._response_back(event, dict(
                code=422,
                detail="'query_embedding' field missed"
            ))
            return

        config = event.payload.get("config")  # indexed configuration
        if not config:
            self._response_back(event, dict(
                code=422,
                detail="'config' field missed"
            ))
            return

        # TODO: calculate cosine distance and return TOP 5 possible commands.

    # --- End Actions ---------------------

    @property
    def is_online(self) -> bool:
        return self._is_launched

    def setup(self, connection_service: ConnectionService):

        self._connection = SyncConnection(self._on_input_event)
        connection_service.add_connection(self.get_topic(None), self._connection)

        self._is_launched = True
