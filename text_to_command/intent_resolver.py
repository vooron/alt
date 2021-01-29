import itertools
import re
from typing import List, NamedTuple, Tuple, Dict

import numpy as np

from text_to_command.command import Command
from text_to_command.configuration_units import SessionConfiguration, SystemConfiguration, SkillsConfiguration
from text_to_command.indexer import Indexer
from text_to_command.parameters import Entry


class DistributionCalculationUnit(NamedTuple):
    command: Command
    distribution: Tuple


class Query:
    CHARS_TO_CLEAR = r"[0-9.,?/()\[\]\":\'#№$\t;<>!+\-_=%]"

    original_query: str
    distribution_query: str
    params_query: str

    distribution_query_parts: List[str]
    params_query_parts: List[str]

    params_to_distribution_query_parts_indices_mapping: Dict[int, int]

    def __init__(self, query: str):
        self.original_query = query.strip()
        self.distribution_query = self._prepare_distribution_query(query)
        self.params_query = self._prepare_params_query(query)
        self.distribution_query_parts = self.distribution_query.split(" ")
        self.params_query_parts = self.params_query.split(" ")
        self.params_to_distribution_query_parts_indices_mapping = self._get_query_parts_mapping()

    def _get_query_parts_mapping(self) -> Dict[int, int]:
        last_params_i = 0
        mapping = {}
        for dist_i, dist_part in enumerate(self.distribution_query_parts):  # dist_query have more strict rules
            for params_i, params_part in enumerate(self.params_query_parts[last_params_i:], start=last_params_i):
                last_params_i = params_i
                if dist_part in params_part:
                    mapping[params_i] = dist_i
                    break
        return mapping

    def _prepare_distribution_query(self, query: str) -> str:
        lc_cleared = query.lower()
        lc_cleared = re.sub(self.CHARS_TO_CLEAR, " ", lc_cleared)
        lc_cleared = re.sub(r'(\w)\'(\w)', "\g<1>\g<2>", lc_cleared)
        lc_cleared = re.sub(r"\s+", " ", lc_cleared)
        return lc_cleared.strip()

    def _prepare_params_query(self, query: str) -> str:
        lc_cleared = query.lower()
        return lc_cleared.strip()



class IntentResolver:  # recommendation system

    indexer: Indexer

    _min_query_ngram_size = 1
    _max_query_ngram_size = 2

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
    def get_candidates_vectors(commands: List[Command], query_tokens_len: int) -> List[Tuple[DistributionCalculationUnit, np.array]]:
        candidates = []
        for command in commands:
            for vector in command.indexed_data.vectors:
                candidates.append(
                    (DistributionCalculationUnit(command, tuple([[] for _ in range(query_tokens_len)])), vector)
                )
        return candidates

    @staticmethod
    def pairwise_cosine_similarity(f_vector, s_vector):
        return np.sum((f_vector * s_vector), axis=1) / (np.linalg.norm(f_vector, axis=1)*np.linalg.norm(s_vector, axis=1))

    @staticmethod
    def get_cartesian_product(
            query_tokens_parts: List[Tuple[Tuple[int, int], np.array]],
            candidates_vectors: List[Tuple[DistributionCalculationUnit, np.array]]
    ) -> Tuple[List[Tuple], List[Tuple]]:
        x = np.tile(np.array(query_tokens_parts, dtype=tuple), (len(candidates_vectors), 1))
        y = np.array(candidates_vectors, dtype=tuple).repeat(len(query_tokens_parts), 0)
        return x, y

    @staticmethod
    def _calculate_parameter_set_score(query_obj: Query, distribution: List[float], parameter_set: List[Tuple[str, Entry]]):
        dist_parts = []

        t_index = 0
        indices = []
        for i, part in  enumerate(query_obj.params_query_parts):
            indices.append((
                i, (t_index, t_index := t_index + len(part))
            ))
            t_index += 1

        n_entries = 0

        for parameter_id, entry in parameter_set:
            for i, (start, end) in indices:
                if (start <= entry.starts_from < end) or (start < entry.ends_at <= end):
                    n_entries += 1
                    if i in query_obj.params_to_distribution_query_parts_indices_mapping:
                        dist_parts.append(query_obj.params_to_distribution_query_parts_indices_mapping[i])
                if entry.ends_at < start:
                    break
        score = 0
        for i in dist_parts:
            score += distribution[i]
        score = score / n_entries
        return score, dist_parts

    def _calculate_distributions(self, query_obj: Query, commands: List[Command]):

        query_tokens = self.indexer.word_2_vec_mapper(query_obj.distribution_query)
        query_tokens_len = len(query_tokens)
        sub_queries_indices = self._spawn_variants(
            list(range(len(query_tokens))),
            min(self._min_query_ngram_size, query_tokens_len - 1),
            min(self._max_query_ngram_size, query_tokens_len - 1)
        )

        query_tokens_parts, candidates_vectors = self.get_cartesian_product(
            [(v, query_tokens[v[0]: v[1] + 1].vector) for v in sub_queries_indices],
            self.get_candidates_vectors(commands, query_tokens_len)
        )

        query_parts_indices, query_parts_vectors = query_tokens_parts[::, 0], query_tokens_parts[::, 1]
        candidates_vectors_indices, candidates_vectors_vectors = candidates_vectors[::, 0], candidates_vectors[::, 1]

        query_parts_vectors = np.array(list(map(lambda x: list(x), query_parts_vectors)))
        candidates_vectors_vectors = np.array(list(map(lambda x: list(x), candidates_vectors_vectors)))

        similarities = self.pairwise_cosine_similarity(query_parts_vectors, candidates_vectors_vectors)

        for query_part_indices, distribution_calc_unit, similarity in zip(
                query_parts_indices, candidates_vectors_indices, similarities):
            for index in range(query_part_indices[0], query_part_indices[1] + 1):
                distribution_calc_unit.distribution[index].append(similarity)

        for distribution_calc_unit in candidates_vectors_indices:
            if not distribution_calc_unit.command.distribution:
                # update distribution for each command
                distribution_calc_unit.command.distribution = [np.mean(d) for d in distribution_calc_unit.distribution]


    def _calculate_parameters(self, query_obj: Query, commands: List[Command]):
        for command in commands:
            parse_from_residuals = []
            all_entries = []
            for parameter in command.parameters:
                if parameter.parse_from_residuals:
                    parse_from_residuals.append(parameter)
                    continue

                entries = parameter.get_entries(query_obj.params_query)

                if not entries:
                    if parameter.default:
                        command.extracted_parameters[parameter.id] = parameter.default.get_value()
                    continue
                all_entries.append([(parameter.id, e) for e in entries])
            score_variants = []

            if all_entries:
                for variant in itertools.product(*all_entries):
                    score, dist_indices = self._calculate_parameter_set_score(query_obj, command.distribution, variant)
                    score_variants.append((variant, score, dist_indices))

                min_score_variant = min(score_variants, key=lambda x: x[1])
                for key, entry in min_score_variant[0]:
                    command.extracted_parameters[key] = entry.value
                    for i in sorted(min_score_variant[2], reverse=True):
                        command.distribution.pop(i)  # remove parameters from dist

    def _calculate_score(self, commands: List[Command]):
        for command in commands:
            dist_score = np.mean(command.distribution)
            required_params_keys_without_default = {p.id for p in command.parameters
                                                    if not p.default and
                                                    not p.parse_from_residuals and
                                                    (not p.choices or not p.choices.is_lazy)}
            if len(required_params_keys_without_default) == 0:
                command.score = dist_score
            else:
                len_required = len(required_params_keys_without_default)
                command.score = 0.7 * dist_score + 0.3 * (
                        len_required -
                        len(required_params_keys_without_default -
                        set(command.extracted_parameters.keys()))
                ) / len_required

    def resolve_intent_recommendations(
            self,
            query: str,
            skills_configuration: SkillsConfiguration,
            system_configuration: SystemConfiguration,
            session_configurations: SessionConfiguration
    ) -> List[Command]:
        self.indexer.ensure_indexed(skills_configuration.skills)
        self.indexer.ensure_indexed(system_configuration.functions)
        self.indexer.ensure_indexed(session_configurations.functions)

        query_obj = Query(query)

        commands = []
        for skill in skills_configuration.skills:
            skill_command = skill.create_command()
            commands.append(skill_command)
            for skill_function in skill.functions:
                commands.append(skill_function.create_command(skill_command))
        commands.extend([f.skill_command() for f in system_configuration.functions])
        commands.extend([f.skill_command() for f in session_configurations.functions])


        self._calculate_distributions(query_obj, commands)
        self._calculate_parameters(query_obj, commands)
        self._calculate_score(commands)

        return commands
