from dataclasses import asdict
from typing import Dict, Callable, Optional

from core.application.function import Function, CommandResponse
from core.skill.index import IndexData, ExactWeightedUnit, EmbeddingWeightedUnit
from text_to_command.indexer import Indexer


class QueryIndexationFunction(Function):
    _get_indexer: Callable[[], Indexer]

    def __init__(self, get_indexer: Callable[[], Indexer]):
        super().__init__()
        self._get_indexer = get_indexer

    def _init_commands(self) -> Dict[str, Callable[[dict, dict], Optional[CommandResponse]]]:
        return {
            "main": self._get_indexed_query
        }

    def _get_indexed_query(self, payload: dict, context: dict, callback: Optional[CommandResponse]):
        print(f"_get_indexed_query({payload.get('user_query')})")
        indexer = self._get_indexer()
        c_text = indexer.clear_string(payload['user_query'])
        embedding = indexer.get_embedding(c_text)

        return CommandResponse(
            payload={
                "query": {
                    "raw": payload['user_query'],
                    "cleared": c_text,
                    "embedding": embedding.tolist() if embedding is not None else None
                }
            },
            context={},
            target=callback.target
        )


class ConfigIndexationFunction(Function):
    _get_indexer: Callable[[], Indexer]

    def __init__(self, get_indexer: Callable[[], Indexer]):
        super().__init__()
        self._get_indexer = get_indexer

    def _init_commands(self) -> Dict[str, Callable[[dict, dict], Optional[CommandResponse]]]:
        return {
            "main": self._get_indexed_data
        }

    def __get_skill_index_data(self, payload: dict) -> IndexData:
        indexer = self._get_indexer()
        exact = [
            ExactWeightedUnit(
                weight=0.5,
                variants=[
                    indexer.clear_string(payload['name'])
                ]
            ),
            ExactWeightedUnit(
                weight=0.3,
                variants=[indexer.clear_string(s) for s in payload['tags']]
            ),
        ]

        embeddings = [
            EmbeddingWeightedUnit(
                weight=0.2,
                embedding=indexer.get_embedding(indexer.clear_string(payload['description'])).tolist()
            )
        ]

        return IndexData(
            exact=exact,
            embeddings=embeddings
        )

    def __get_skill_function_index_data(self, payload: dict) -> IndexData:
        indexer = self._get_indexer()
        exact = [
            ExactWeightedUnit(
                weight=0.4,
                variants=[
                    indexer.clear_string(payload['name'])
                ]
            ),
        ]

        embeddings = [
            EmbeddingWeightedUnit(
                weight=0.2,
                embedding=indexer.get_embedding(indexer.clear_string(payload['description'])).tolist()
            )
        ]

        call_example_embeddings = list(filter(lambda x: x is not None, [
            indexer.get_embedding(indexer.clear_string(e)) for e in payload['call_examples']
        ]))

        if call_example_embeddings:
            final_call_example_embedding = call_example_embeddings[0]
            for e in call_example_embeddings[1:]:
                final_call_example_embedding += e

            embeddings.append(
                EmbeddingWeightedUnit(
                    weight=0.4,
                    embedding=final_call_example_embedding.tolist()
                )
            )

        return IndexData(
            exact=exact,
            embeddings=embeddings
        )

    def _get_indexed_data(self, payload: dict, context: dict, callback: Optional[CommandResponse]):
        """
        payload: {
            (id: str): {
                type: ENUM("SKILL_FUNCTION", "SKILL"),

                name: str,
                description: str

                # for SKILL_FUNCTION
                call_examples: List[str]
                # end for SKILL_FUNCTION

                # for SKILL
                tags: List[str]
                # end for SKILL
            },
            ...
        }
        """
        result = {}
        for unit_id, params in payload.items():
            if params['type'] == 'SKILL':
                result[unit_id] = asdict(self.__get_skill_index_data(params))
            else:
                result[unit_id] = asdict(self.__get_skill_function_index_data(params))

        return CommandResponse(
            payload=result,
            context={},
            target=callback.target
        )
