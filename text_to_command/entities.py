from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from .parameters import Parameter, ParameterDeserializer

parameter_deserializer = ParameterDeserializer()


@dataclass
class ParametersSet:
    identifier_code: str
    parameters: List[Parameter]

    def to_dict(self):
        return dict(
            identifier_code=self.identifier_code,
            parameters=[p.to_dict() for p in self.parameters]
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            identifier_code=data['identifier_code'],
            parameters=[parameter_deserializer.from_dict(p) for p in data['parameters']]
        )


@dataclass
class IndexedData:
    cleared_lc: str
    general_vector: np.array


@dataclass
class FunctionIndex:
    name_index: IndexedData
    description_index: IndexedData
    call_examples_index: List[IndexedData]


@dataclass
class ApplicationIndex:
    name_index: IndexedData
    description_index: IndexedData
    tags_index: List[IndexedData]


@dataclass
class Function:
    identifier_code: str
    name: str
    description: str
    call_examples: List[str]
    parameters_set_list: List[ParametersSet]

    application: Optional['Application']

    indexed_data: Optional[FunctionIndex]

    def __init__(self, identifier_code: str, name: str,
                 description: str, call_examples: List[str],
                 parameters_set_list: List[ParametersSet],
                 indexed_data: FunctionIndex = None):
        self.identifier_code = identifier_code
        self.name = name
        self.description = description
        self.call_examples = call_examples
        self.indexed_data = indexed_data
        self.parameters_set_list = parameters_set_list

    def get_identifier(self):
        if self.application:
            return self.application.get_identifier() + "." + self.identifier_code
        else:
            return self.identifier_code

    def to_dict(self):
        return dict(
            identifier_code=self.identifier_code,
            name=self.name,
            description=self.description,
            call_examples=self.call_examples,
            parameters_set_list=[ps.to_dict() for ps in self.parameters_set_list]
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            identifier_code=data['identifier_code'],
            name=data['name'],
            description=data['description'],
            call_examples=data['call_examples'],
            parameters_set_list=[ParametersSet.from_dict(p) for p in data['parameters_set_list']]
        )


@dataclass
class Application:
    identifier_code: str
    name: str
    description: str
    tags: List[str]
    functions: List[Function]

    indexed_data: ApplicationIndex

    def __init__(self, identifier_code: str, name: str, description: str, tags: List[str], functions: List[Function],
                 indexed_data: ApplicationIndex = None):
        self.identifier_code = identifier_code
        self.name = name
        self.description = description
        self.tags = tags
        self.functions = functions

        self.indexed_data = indexed_data

        for function in functions:
            function.application = self

    def get_identifier(self):
        return self.identifier_code

    def to_dict(self):
        return dict(
            identifier_code=self.identifier_code,
            name=self.name,
            description=self.description,
            tags=self.tags,
            functions=[f.to_dict() for f in self.functions]
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            identifier_code=data['identifier_code'],
            name=data['name'],
            description=data['description'],
            tags=data['tags'],
            functions=[Function.from_dict(p) for p in data['functions']]
        )


@dataclass
class AppsConfiguration:
    applications: List[Application]

    def to_dict(self):
        return dict(
            applications=[a.to_dict() for a in self.applications]
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            applications=[Application.from_dict(a) for a in data['applications']]
        )


@dataclass
class SystemConfiguration:
    functions: List[Function]


@dataclass
class SessionConfiguration:
    app_identifier_code: str
    functions: List[Function]
