from typing import Dict, Callable, Optional, List

import numpy as np
import pandas as pd
from Levenshtein import distance

from core.application.function import Function, CommandResponse
from core.communication.callback import Callback


class UserQueryProcessingFunction(Function):

    def _init_commands(self) -> Dict[str, Callable[[dict, dict, Optional[Callback]], Optional[CommandResponse]]]:
        return {
            "getRating": self._get_rating
        }

    def __get_exact_df(self, config: dict) -> pd.DataFrame:
        exact_data = []

        for config_id in config.keys():
            exact_data.extend([
                dict(zip(("id", "weight", "variants"), (config_id, *weighed_pair)))
                for weighed_pair in config[config_id]['exact']
            ])

        return pd.DataFrame(exact_data)

    def __get_embedding_df(self, config: dict) -> pd.DataFrame:
        embedding_data = []

        for config_id in config.keys():
            embedding_data.extend([
                dict(zip(("id", "weight", "embedding"), (config_id, *weighed_pair)))
                for weighed_pair in config[config_id]['embeddings']
            ])

        return pd.DataFrame(embedding_data)

    def _get_rating(self, payload: dict, context: dict, callback: Optional[Callback]) -> Optional[CommandResponse]:
        """Main
        payload: {
            query: {
                raw: str,
                cleared: str,
                embedding: list
            },
            config: {
                (id: str): {
                    exact: [
                        (weight: float, variants: list),
                        ...
                    ],
                    embedding: [
                        (weight: float, embedding: list),
                        ...
                    ]
                }
            }
        }
        """
        skill_score_weight = 0.2

        query_cleared = payload['query']['cleared']
        query_embedding = payload['query']['embedding']

        exact_df = self.__get_exact_df(payload['config'])
        exact_df['similarity'] = exact_df['variants'].map(calculate_exact_similarity(query_cleared))

        embedding_df = self.__get_embedding_df(payload['config'])
        embedding_df['similarity'] = embedding_df['embedding'].map(calculate_embedding_similarity(query_embedding))

        common_columns = ['id', 'weight', 'similarity']
        common_df = pd.concat([
            exact_df[common_columns],
            embedding_df[common_columns]
        ], ignore_index=True)

        common_df['weighted_similarity'] = common_df['weight'] * common_df['similarity']
        grouped = common_df.groupby("id")['weighted_similarity'].sum()

        calculated_dict = grouped.to_dict()

        # correct weights to take skill for function score calculation
        for key, similarity in calculated_dict.items():
            if "." in key:
                skill_id, function_id = key.split(".")
                calculated_dict[key] = skill_score_weight * calculated_dict[skill_id] + (1 - skill_score_weight) * \
                                       calculated_dict[key]

        for key, similarity in sorted(calculated_dict.items(), key=lambda x: x[1], reverse=True)[:5]:
            print(key, similarity)


def calculate_exact_similarity(query: str):
    def internal(variants: List[str]):
        similarity_score = 0
        for variant in variants:
            candidate_score = 1 - distance(query, variant) / max(len(query), len(variant))
            if candidate_score > similarity_score:
                similarity_score = candidate_score
        return similarity_score

    return internal


def calculate_embedding_similarity(query_embedding: np.array):
    def internal(embedding: list):
        np_embedding = np.array(embedding)
        return max(
            0,
            np.dot(query_embedding, np_embedding) / (np.linalg.norm(query_embedding) * np.linalg.norm(np_embedding))
        )

    return internal
