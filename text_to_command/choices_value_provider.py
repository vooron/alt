from dataclasses import dataclass
from typing import NamedTuple, List, Any


class ChoiceValue(NamedTuple):
    label: str
    value: Any

    def to_dict(self):
        return dict(
            label=self.label,
            value=self.value,
        )


@dataclass
class ChoicesValueProvider:
    values: List[ChoiceValue]
    is_lazy: bool

    def is_entry_in(self, value: Any) -> bool:
        for choice_value in self.values:
            if value == choice_value.value:
                return True
        return False
