from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import NamedTuple, List, Any

import Levenshtein


class ChoiceValue(NamedTuple):
    label: str
    value: str

    def to_dict(self):
        return dict(
            label=self.label,
            value=self.value,
        )


class ChoicesValueProviderType(Enum):
    CONSTANT = 'CONSTANT'


class ChoicesValueProvider(metaclass=ABCMeta):
    type: ChoicesValueProviderType

    @abstractmethod
    def get_values(self) -> List[ChoiceValue]:
        pass

    def is_in(self, value: Any):
        return value in self.get_values()

    def get_nearest_candidates(self, value: Any):
        return list(
            sorted(
                [(c, Levenshtein.distance(value, c.label)) for c in self.get_values()],
                key=lambda x: x[1],
                reverse=True
            )
        )[0:5]

    def to_dict(self):
        return dict(
            type=self.type.value
        )

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        pass

    def __str__(self):
        return f"ChoicesValueProvider:{self.type.name}()"


@dataclass
class ConstantChoicesValueProvider(ChoicesValueProvider):
    values: List[ChoiceValue]
    type = ChoicesValueProviderType.CONSTANT

    def get_values(self) -> List[ChoiceValue]:
        return self.values

    def to_dict(self):
        return dict(
            **super(ConstantChoicesValueProvider, self).to_dict(),
            values=[v.to_dict() for v in self.values]
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            values=[ChoiceValue(label=v['label'], value=v['value']) for v in data['values']]
        )


class ChoicesValueProviderDeserializer:

    mapping = {
        ChoicesValueProviderType.CONSTANT: ConstantChoicesValueProvider
    }

    def from_dict(self, data: dict) -> ChoicesValueProvider:
        return self.mapping[ChoicesValueProviderType(data['type'])].from_dict(data)
