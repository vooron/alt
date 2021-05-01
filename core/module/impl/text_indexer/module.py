from typing import Dict, Callable

import spacy

from core.communication.connection import Connection, SyncConnection
from core.communication.connection_service import ConnectionService
from core.communication.message import Message
from core.module.module import Module
from text_to_command.indexer import Indexer


class TextIndexerModule(Module):
    MODULE_ID = "TextIndexer"

    _is_launched: bool = False
    _indexer: Indexer

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
        text = event.payload.get("text")
        if not text:
            self._response_back(event, dict(
                code=422,
                detail="'text' field missed"
            ))
            return
        c_text = self._indexer.clear_string(text)
        embedding = self._indexer.get_embedding(c_text)
        self._response_back(event, dict(
            type="Error",
            code=200,  # TODO: add error codes
            data=dict(
                embedding=embedding
            )
        ))
    # --- End Actions ---------------------

    @property
    def is_online(self) -> bool:
        return self._is_launched

    def setup(self, connection_service: ConnectionService):
        self._indexer = Indexer(spacy.load("en_core_web_md"))

        self._connection = SyncConnection(self._on_input_event)
        connection_service.add_connection(self.get_topic(None), self._connection)

        self._is_launched = True
