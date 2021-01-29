from abc import abstractmethod, ABCMeta
from typing import Any


class ParameterValueProvider(metaclass=ABCMeta):

    @abstractmethod
    def get_value(self):
        pass


class ConstantParameterValueProvider(ParameterValueProvider):
    value: Any

    def __init__(self, value):
        self.value = value

    def get_value(self):
        return self.value

