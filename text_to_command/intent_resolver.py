import re
from typing import Any, List, Union, Tuple

import numpy as np
import spacy

from text_to_command.entities import AppsConfiguration, SystemConfiguration, SessionConfiguration, Function, \
    FunctionIndex, IndexedData, Application, ApplicationIndex
from text_to_command.main import apps_config_factory


class Indexer:
    word_2_vec_mapper: Any  # spacy.lang.en.English for now

    def __init__(self, word_2_vec_mapper: Any):
        self.word_2_vec_mapper = word_2_vec_mapper

    @staticmethod
    def clear_string(data: str) -> str:
        lc_cleared = data.lower()
        lc_cleared = re.sub(r"[.,?/()\[\]\'\"]", " ", lc_cleared)
        lc_cleared = re.sub(r"\s+", " ", lc_cleared)
        return lc_cleared.strip()

    def get_index_function_data(self, function: Function):
        cleared_lc_name = self.clear_string(function.name)
        cleared_lc_description = self.clear_string(function.description)

        cleared_lc_call_examples = [
            self.clear_string(call_example) for call_example in function.call_examples]

        return FunctionIndex(
            name_index=IndexedData(
                cleared_lc=cleared_lc_name,
                general_vector=self.word_2_vec_mapper(cleared_lc_name).vector
            ),
            description_index=IndexedData(
                cleared_lc=cleared_lc_description,
                general_vector=self.word_2_vec_mapper(cleared_lc_description).vector
            ),
            call_examples_index=[IndexedData(
                cleared_lc=call_example,
                general_vector=self.word_2_vec_mapper(call_example).vector
            ) for call_example in cleared_lc_call_examples]
        )

    def get_index_application_data(self, application: Application):
        cleared_lc_name = self.clear_string(application.name)
        cleared_lc_description = self.clear_string(application.description)

        cleared_lc_tags = [
            self.clear_string(tag) for tag in application.tags]

        return ApplicationIndex(
            name_index=IndexedData(
                cleared_lc=cleared_lc_name,
                general_vector=self.word_2_vec_mapper(cleared_lc_name)
            ),
            description_index=IndexedData(
                cleared_lc=cleared_lc_description,
                general_vector=self.word_2_vec_mapper(cleared_lc_description)
            ),
            tags_index=[IndexedData(
                cleared_lc=tag,
                general_vector=self.word_2_vec_mapper(tag).vector
            ) for tag in cleared_lc_tags]
        )

    def ensure_indexed(self, configuration_entries: List[Union[Function, Application]]):
        for configuration_entry in configuration_entries:

            if isinstance(configuration_entry, Function):
                if not configuration_entry.indexed_data:
                    configuration_entry.indexed_data = self.get_index_function_data(configuration_entry)
            elif isinstance(configuration_entry, Application):
                if not configuration_entry.indexed_data:
                    configuration_entry.indexed_data = self.get_index_application_data(configuration_entry)
                self.ensure_indexed(configuration_entry.functions)


class IntentResolver:  # recommendation system

    indexer: Indexer

    _min_query_ngram_size = 1
    _max_query_ngram_size = 3

    def __init__(self, indexer: Indexer):
        self.indexer = indexer

    @staticmethod
    def _spawn_variants(indices: List[int], min_size: int, max_size: int) -> List[Tuple[int, int]]:
        result = []
        for size in range(min_size, max_size + 1):
            for i in range(len(indices) - size + 1):
                result.append(
                    (indices[i], indices[i + size - 1])
                )
        return result

    @staticmethod
    def get_candidates_vectors(apps_configuration: List[Application], *other_configs):
        candidates_vectors = {}
        for app in apps_configuration:
            candidates_vectors[app.get_identifier()] = [
                app.indexed_data.name_index.general_vector, app.indexed_data.description_index.general_vector,
                *[t.general_vector for t in app.indexed_data.tags_index]
            ]
            for function in app.functions:
                candidates_vectors[function.get_identifier()] = [
                    function.indexed_data.name_index.general_vector,
                    function.indexed_data.description_index.general_vector,
                    *[ce.general_vector for ce in function.indexed_data.call_examples_index]
                ]
        return candidates_vectors

    @staticmethod
    def get_cartesian_product(query_tokens_parts, candidates_vectors) -> Tuple[List[Tuple], List[Tuple]]:
        x = np.tile(query_tokens_parts, len(candidates_vectors))
        y = np.repeat(candidates_vectors, len(query_tokens_parts))
        return x, y

    def resolve_intent_recommendations(
            self,
            query: str,
            apps_configuration: AppsConfiguration,
            system_configuration: SystemConfiguration,
            session_configurations: SessionConfiguration
    ):
        self.indexer.ensure_indexed(apps_configuration.applications)

        query = self.indexer.clear_string(query)
        query_parts = query.split(" ")

        query_tokens = self.indexer.word_2_vec_mapper(query)
        variants = self._spawn_variants(
            list(range(len(query_parts))),
            min(self._min_query_ngram_size, len(query_parts) - 1),
            min(self._max_query_ngram_size, len(query_parts) - 1)
        )

        print("==", query)
        for q in [(v, query_tokens[v[0]: v[1] + 1].vector) for v in variants]:
            print(q)


indexer = Indexer(spacy.load("en_core_web_md"))
intent_resolver = IntentResolver(indexer)

intent_resolver.resolve_intent_recommendations(
    "Send Ann a message 'Buy some potato' with Telegram",
    apps_config_factory(),
    None, None
)
