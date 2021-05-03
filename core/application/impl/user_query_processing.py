import json
import logging
from typing import Dict, Callable, Optional, List

from core.application.application import Application
from core.application.function import Function, CommandResponse
from core.communication.callback import Callback
from core.communication.command_identifier import CommandIdentifier, ApplicationType
from core.communication.connection import SyncConnection
from core.communication.connection_service import ConnectionService
from core.communication.message import Message
from core.skill.function_configuration import FunctionConfiguration
from core.skill.index import IndexData
from core.skill.skill_configuration import SkillConfiguration


class UserQueryProcessing(Application):
    config_file: str = "skills_config.json"
    skills_config: Dict[str, SkillConfiguration]  # probably needed to be moved to controller or storage

    def __init__(self, id: str):
        super().__init__(id, ApplicationType.CORE)

    def _init_functions(self) -> Dict[str, Function]:
        return {
            "saveConfigIndexingFunction": SaveConfigIndexingFunction(self),
            "processUserQueryFunction": ProcessUserQueryFunction(self)
        }

    def __serialize_config(self, config: List[SkillConfiguration]) -> str:
        result = []
        for skill in config:
            result.append(skill.to_dict())
        return json.dumps(result)

    def __deserialize_config(self, data: List[dict]) -> List[SkillConfiguration]:
        result = []
        for config_data in data:
            functions = [FunctionConfiguration(
                name=f['name'],
                description=f['description'],
                call_examples=f['call_examples'],
                indexed_data=IndexData.from_dict(f['indexed_data']) if f['indexed_data'] else None
            ) for f in config_data['functions']]

            result.append(SkillConfiguration(
                name=config_data['name'],
                description=config_data['description'],
                tags=config_data['tags'],
                functions=functions,
                indexed_data=IndexData.from_dict(config_data['indexed_data']) if config_data['indexed_data'] else None
            ))

        return result

    def update_config(self, config: Dict[str, SkillConfiguration]):
        self.skills_config = config
        with open(self.config_file, 'w') as f:
            f.write(self.__serialize_config(list(config.values())))

    def __ensure_indexed(self, connection_service: ConnectionService):
        to_be_indexed = {}
        for skill_id, skill in self.skills_config.items():
            if not skill.indexed_data:
                to_be_indexed[skill_id] = {
                    "type": "SKILL",
                    "name": skill.name,
                    "description": skill.description,
                    "tags": skill.tags
                }
            for function_id, function in skill.functions.items():
                if not function.indexed_data:
                    to_be_indexed[function.id] = {
                        "type": "SKILL_FUNCTION",
                        "name": function.name,
                        "description": function.description,
                        "call_examples": function.call_examples
                    }

        if not to_be_indexed.keys():
            return

        connection_service.dispatch(Message(
            payload=to_be_indexed,
            target=CommandIdentifier(ApplicationType.MODULE, "TextIndexer", "configIndexationFunction", "main"),
            source=CommandIdentifier(ApplicationType.CORE, self.id, None, None),
            context={},
            callback=Callback(
                target=CommandIdentifier(
                    ApplicationType.CORE, self.id, "saveConfigIndexingFunction", "main"
                )
            )
        ))

    def setup(self, connection_service: ConnectionService):

        self._connection = SyncConnection(self._on_event)
        connection_service.add_connection(self.application_type, self.id, self._connection)

        with open(self.config_file) as f:
            data = json.load(f)

        self.skills_config = {s.id: s for s in self.__deserialize_config(data)}
        self.__ensure_indexed(connection_service)


class SaveConfigIndexingFunction(Function):
    _application: UserQueryProcessing

    def __init__(self, application: UserQueryProcessing):
        super().__init__()
        self._application = application

    def _init_commands(self) -> Dict[str, Callable[[dict, dict, Optional[Callback]], Optional[CommandResponse]]]:
        return {
            "main": self._save_index_data
        }

    def _save_index_data(self, payload: dict, context: dict, callback: Optional[Callback]):
        logging.info(f"New indexed entities: {len(payload.keys())}")
        config = self._application.skills_config
        for entity_id, indexed_data in payload.items():
            if "." in entity_id:
                skill_id, function_id = entity_id.split(".")
                config[skill_id].functions[function_id].indexed_data = IndexData.from_dict(indexed_data)
            else:
                config[entity_id].indexed_data = IndexData.from_dict(indexed_data)
        self._application.update_config(config)


class ProcessUserQueryFunction(Function):
    _application: UserQueryProcessing

    def __init__(self, application: UserQueryProcessing):
        super().__init__()
        self._application = application

    def _init_commands(self) -> Dict[str, Callable[[dict, dict, Optional[Callback]], Optional[CommandResponse]]]:
        return {
            "main": self._on_user_query,
            "onQueryIndexed": self._on_query_indexed,
            "onCommandsRating": self._on_commands_rating
        }

    def _on_commands_rating(
            self, payload: dict, context: dict, callback: Optional[Callback]
    ) -> Optional[CommandResponse]:
        print("===========================================", flush=True)
        for key, value in payload.items():
            print(f"   {key}: {value}")
        return

    def _on_user_query(self, payload: dict, context: dict, callback: Optional[Callback]) -> Optional[CommandResponse]:
        return CommandResponse(
            payload=payload,
            context={},
            target=CommandIdentifier(
                ApplicationType.MODULE, "TextIndexer", "queryIndexation", "main"
            ),
            callback=Callback(CommandIdentifier(
                ApplicationType.CORE, self._application.id, "processUserQueryFunction", "onQueryIndexed"
            ))
        )

    def _on_query_indexed(
            self, payload: dict, context: dict, callback: Optional[Callback]
    ) -> Optional[CommandResponse]:

        if not payload['query']['embedding']:
            logging.error(f"Query {payload['query']['raw']} has no embedding.")
            return

        config = {}

        for skill_id, skill in self._application.skills_config.items():
            if skill.indexed_data:
                config[skill.id] = skill.indexed_data.to_dict()

            for function_id, function in skill.functions.items():
                if function.indexed_data:
                    config[function.id] = function.indexed_data.to_dict()

        return CommandResponse(
            payload={
                "query": payload['query'],
                "config": config
            },
            context={},
            target=CommandIdentifier(ApplicationType.MODULE, "TextToCommand", "getSkillsRatingByQuery", "main"),
            callback=Callback(CommandIdentifier(
                ApplicationType.CORE, self._application.id, "processUserQueryFunction", "onCommandsRating"
            ))
        )
