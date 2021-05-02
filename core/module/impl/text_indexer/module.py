from typing import Dict

import spacy

from core.application.function import Function
from core.communication.connection import SyncConnection
from core.communication.connection_service import ConnectionService
from core.module.impl.text_indexer.functions import IndexationFunction
from core.module.module import Module
from text_to_command.indexer import Indexer


class TextIndexerModule(Module):
    _indexer: Indexer

    def _init_functions(self) -> Dict[str, Function]:
        return {
            "indexation": IndexationFunction(lambda: self._indexer)
        }

    def setup(self, connection_service: ConnectionService):
        self._indexer = Indexer(spacy.load("en_core_web_md"))

        self._connection = SyncConnection(self._on_event)
        connection_service.add_connection(self.application_type, self.id, self._connection)
