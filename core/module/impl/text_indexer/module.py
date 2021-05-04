from typing import Dict, Callable

import spacy

from core.application.function import Function
from core.communication.connection import SyncConnection
from core.communication.connection_service import ConnectionService
from core.module.impl.text_indexer.functions import ConfigIndexationFunction, QueryIndexationFunction
from core.module.module import Module
from text_to_command.indexer import Indexer


class TextIndexerModule(Module):

    _indexer: Indexer

    def _init_functions(self) -> Dict[str, Function]:
        return {
            "configIndexationFunction": ConfigIndexationFunction(lambda: self._indexer),
            "queryIndexation": QueryIndexationFunction(lambda: self._indexer)
        }

    def register_cycle_handlers(self, register_cycle_handler: Callable[[Callable[[], None]], None]):
        pass

    def setup(self, connection_service: ConnectionService):
        self._indexer = Indexer(spacy.load("en_core_web_md"))

        self._connection = SyncConnection(self._on_event)
        connection_service.add_connection(self.application_type, self.id, self._connection)
