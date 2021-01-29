from dataclasses import dataclass
from typing import List, Optional

import numpy as np

from .parameters import Parameter


@dataclass
class IndexedData:
    vectors: List[np.array]  # multiple word2vec vectors to all tags, call examples, etc.


@dataclass
class SkillFunction:
    id: str
    name: str
    description: str
    call_examples: List[str]
    parameters: List[Parameter]

    indexed_data: Optional[IndexedData]

    def __init__(self, id: str, name: str,
                 description: str, call_examples: List[str],
                 parameters: List[Parameter],
                 indexed_data: IndexedData = None):
        self.id = id
        self.name = name
        self.description = description
        self.call_examples = call_examples
        self.indexed_data = indexed_data
        self.parameters = parameters

    def create_command(self, skill_command: 'SkillCommand' = None):
        from .command import SkillFunctionCommand
        return SkillFunctionCommand(skill_command, self, None)


@dataclass
class SkillConfiguration:
    id: str
    name: str
    description: str
    tags: List[str]
    functions: List[SkillFunction]

    indexed_data: IndexedData

    def __init__(self, id: str, name: str, description: str, tags: List[str], functions: List[SkillFunction],
                 indexed_data: IndexedData = None):
        self.id = id
        self.name = name
        self.description = description
        self.tags = tags
        self.functions = functions

        self.indexed_data = indexed_data

    def create_command(self):
        from .command import SkillCommand
        return SkillCommand(self, None)


@dataclass
class SkillsConfiguration:
    skills: List[SkillConfiguration]


@dataclass
class SystemConfiguration:
    functions: List[SkillFunction]


@dataclass
class SessionConfiguration:
    skill_identifier_code: str
    functions: List[SkillFunction]
