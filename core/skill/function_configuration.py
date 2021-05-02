from typing import List

from slugify import slugify


class FunctionConfiguration:
    _id: str
    skill_id: str = None

    name: str
    description: str
    call_examples: List[str]

    # parameters: list

    def __init__(
            self,
            name: str,
            description: str,
            call_examples: List[str]
    ):
        self._id = slugify(name)
        self.name = name
        self.description = description
        self.call_examples = call_examples

    @property
    def id(self):
        if self.skill_id:
            return self.skill_id + "." + self._id

        return self._id
