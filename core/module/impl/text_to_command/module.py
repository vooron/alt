from typing import Dict, Callable

from core.application.function import Function
from core.communication.connection import Connection, SyncConnection
from core.communication.connection_service import ConnectionService
from core.module.impl.text_to_command.functions import GetSkillsRatingByQueryFunction
from core.module.module import Module


class TextToCommandModule(Module):

    _connection: Connection

    def _init_functions(self) -> Dict[str, Function]:
        return {
            "getSkillsRatingByQuery": GetSkillsRatingByQueryFunction()
        }

    def setup(self, connection_service: ConnectionService):
        self._connection = SyncConnection(self._on_event)
        connection_service.add_connection(self.application_type, self.id, self._connection)

    def register_cycle_handlers(self, register_cycle_handler: Callable[[Callable[[], None]], None]):
        pass
