import json
from dataclasses import dataclass, asdict
from typing import Dict, List, Tuple, NamedTuple


class ExactWeightedUnit(NamedTuple):
    weight: float
    variants: List[str]


class EmbeddingWeightedUnit(NamedTuple):
    weight: float
    embedding: list


@dataclass
class IndexData:
    exact: List[ExactWeightedUnit]
    embeddings: List[EmbeddingWeightedUnit]

    def __init__(self, exact: List[ExactWeightedUnit], embeddings: List[EmbeddingWeightedUnit]):
        if not self.is_weights_valid(exact, embeddings):
            raise ValueError("Index weights corrupted.")
        self.exact = exact
        self.embeddings = embeddings

    @staticmethod
    def is_weights_valid(exact: List[ExactWeightedUnit], embeddings: List[EmbeddingWeightedUnit]) -> bool:
        weights_sum = 0
        for unit in exact:
            weights_sum += unit.weight

        for unit in embeddings:
            weights_sum += unit.weight

        eps = 0.001
        target_value = 1

        return target_value - eps <= weights_sum <= target_value + eps

    def serialize(self) -> str:
        return json.dumps(asdict(self))

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'IndexData':
        exact = []
        embeddings = []

        for unit in data['exact']:
            exact.append(ExactWeightedUnit(*unit))

        for unit in data['embeddings']:
            embeddings.append(EmbeddingWeightedUnit(*unit))

        return cls(exact=exact, embeddings=embeddings)
