from typing import List

from slugify import slugify

from core.skill.index import IndexData


class FunctionConfiguration:
    _id: str
    skill_id: str = None

    name: str
    description: str
    call_examples: List[str]

    indexed_data: IndexData
    # parameters: list

    def __init__(
            self,
            name: str,
            description: str,
            call_examples: List[str],
            indexed_data: IndexData = None
    ):
        self._id = slugify(name)
        self.name = name
        self.description = description
        self.call_examples = call_examples
        self.indexed_data = indexed_data

    @property
    def id(self):
        if self.skill_id:
            return self.skill_id + "." + self._id

        return self._id

    def to_dict(self) -> dict:
        return dict(
            id=self._id,
            name=self.name,
            description=self.description,
            call_examples=self.call_examples,
            indexed_data=self.indexed_data.to_dict() if self.indexed_data else None
        )

