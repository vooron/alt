from abc import abstractmethod, ABCMeta
from typing import Optional, List

import numpy as np

from text_to_command.configuration_units import SkillConfiguration, SkillFunction, IndexedData
from text_to_command.parameters import Parameter


class Command(metaclass=ABCMeta):
    # add priority coefficient
    distribution: list  # 1d
    extracted_parameters: dict
    score: float  # [0, 1]

    def __init__(self, distribution: list):
        self.distribution = distribution
        self.extracted_parameters = {}
        self.score = 0

    @property
    @abstractmethod
    def descriptive_name(self) -> str:
        pass

    @property
    @abstractmethod
    def indexed_data(self) -> IndexedData:
        pass

    @property
    def parameters(self) -> List[Parameter]:
        return []


class SkillCommand(Command):
    skill: SkillConfiguration

    def __init__(self, skill: SkillConfiguration, distribution: np.array):
        super(SkillCommand, self).__init__(distribution)
        self.skill = skill

    @property
    def indexed_data(self) -> IndexedData:
        return self.skill.indexed_data

    @property
    def descriptive_name(self) -> str:
        return self.skill.name + " | " + str(self.extracted_parameters)

    def __str__(self):
        return f"SkillCommand(id={self.skill.name}, distribution=f{self.distribution}, params={self.extracted_parameters})"


class SkillFunctionCommand(Command):
    skill_command: Optional[SkillCommand]
    function: SkillFunction

    def __init__(self, skill_command: Optional[SkillCommand], function: SkillFunction, distribution: np.array):
        super(SkillFunctionCommand, self).__init__(distribution)
        self.skill_command = skill_command
        self.function = function

    @property
    def indexed_data(self) -> IndexedData:
        # join both vectors to make
        return IndexedData(vectors=self.function.indexed_data.vectors + self.skill_command.indexed_data.vectors)

    @property
    def descriptive_name(self) -> str:
        return self.skill_command.skill.name + "." + self.function.name + " | " + str(self.extracted_parameters)

    @property
    def parameters(self) -> List[Parameter]:
        return self.function.parameters

    def __str__(self):
        return f"SkillFunctionCommand(id={self.skill_command.skill.id}.{self.function.name}," \
               f" distribution=f{self.distribution}, params={self.extracted_parameters})"
