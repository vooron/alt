import re
from typing import Any, List, Union

from text_to_command.configuration_units import SkillFunction, IndexedData, SkillConfiguration


class Indexer:
    word_2_vec_mapper: Any  # spacy.lang.en.English for now

    def __init__(self, word_2_vec_mapper: Any):
        self.word_2_vec_mapper = word_2_vec_mapper

    @staticmethod
    def clear_string(data: str) -> str:
        lc_cleared = data.lower()
        lc_cleared = re.sub(r"[0-9.,?/()\[\]\'\":#№$\t;<>!+\-_=%]", " ", lc_cleared)
        lc_cleared = re.sub(r"\s+", " ", lc_cleared)
        return lc_cleared.strip()

    def get_embedding(self, s: str):
        token = self.word_2_vec_mapper(s)
        if token.has_vector:
            return token.vector

    def get_index_function_data(self, function: SkillFunction):
        data = [
            self.clear_string(function.name),
            *[self.clear_string(call_example) for call_example in function.call_examples]
        ]

        vectors = []
        for s in data:
            token = self.word_2_vec_mapper(s)
            if token.has_vector:
                vectors.append(token.vector)
        return IndexedData(
            vectors=vectors
        )

    def get_index_application_data(self, skill: SkillConfiguration):
        data = [
            self.clear_string(skill.name),
            *[self.clear_string(tag) for tag in skill.tags]
        ]
        vectors = []
        for s in data:
            token = self.word_2_vec_mapper(s)
            if token.has_vector:
                vectors.append(token.vector)
        return IndexedData(
            vectors=vectors
        )

    def ensure_indexed(self, configuration_entries: List[Union[SkillFunction, SkillConfiguration]]):
        for configuration_entry in configuration_entries:

            if isinstance(configuration_entry, SkillFunction):
                if not configuration_entry.indexed_data:
                    configuration_entry.indexed_data = self.get_index_function_data(configuration_entry)
            elif isinstance(configuration_entry, SkillConfiguration):
                if not configuration_entry.indexed_data:
                    configuration_entry.indexed_data = self.get_index_application_data(configuration_entry)
                self.ensure_indexed(configuration_entry.functions)
