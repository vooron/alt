from abc import abstractmethod, ABCMeta
from enum import Enum
from typing import Any


class ParameterValueProviderType(Enum):
    CONSTANT = 'CONSTANT'


class ParameterValueProvider(metaclass=ABCMeta):
    type: ParameterValueProviderType

    @abstractmethod
    def get_value(self):
        pass

    def to_dict(self):
        return dict(
            type=self.type.value
        )

    @classmethod
    @abstractmethod
    def from_dict(cls, data: dict):
        pass

    def __str__(self):
        return f"ParameterValueProvider:{self.type.name}()"


class ConstantParameterValueProvider(ParameterValueProvider):
    value: Any
    type = ParameterValueProviderType.CONSTANT

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

    def to_dict(self):
        return dict(
            **super(ConstantParameterValueProvider, self).to_dict(),
            value=self.value,
        )

    @classmethod
    def from_dict(cls, data: dict):
        print("---", data)
        return cls(data['value'])


class ParameterValueProviderDeserializer:
    mapping = {
        ParameterValueProviderType.CONSTANT: ConstantParameterValueProvider
    }

    def from_dict(self, data: dict) -> ParameterValueProvider:
        return self.mapping[ParameterValueProviderType(data['type'])].from_dict(data)
