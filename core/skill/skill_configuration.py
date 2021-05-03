from typing import List, Dict

from slugify import slugify

from core.skill.function_configuration import FunctionConfiguration
from core.skill.index import IndexData


class SkillConfiguration:
    id: str

    # descriptive
    name: str
    description: str
    tags: List[str]

    functions: Dict[str, FunctionConfiguration]

    indexed_data: IndexData = None

    def __init__(
            self,
            name: str,
            description: str,
            tags: List[str],
            functions: List[FunctionConfiguration],
            indexed_data: IndexData = None
    ):
        self.id = slugify(name)
        self.name = name
        self.description = description
        self.tags = tags
        self.functions = {f.id: f for f in functions}

        for function in functions:
            function.skill_id = self.id

        self.indexed_data = indexed_data

    def to_dict(self) -> dict:
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
            tags=self.tags,
            functions=[f.to_dict() for f in self.functions.values()],
            indexed_data=self.indexed_data.to_dict() if self.indexed_data else None
        )
