import itertools
import re
from abc import ABCMeta, abstractmethod
from datetime import date, timedelta
from typing import Optional, NamedTuple, Any, List, Dict

from .choices_value_provider import ChoicesValueProvider
from .parameter_value_provider import ParameterValueProvider, ConstantParameterValueProvider


class Entry(NamedTuple):
    starts_from: int
    ends_at: int
    value: Any


class Parameter(metaclass=ABCMeta):
    id: str
    name: str
    default: Optional[ParameterValueProvider]
    choices: Optional[ChoicesValueProvider]
    parse_from_residuals: bool = False

    def __init__(
            self,
            id: str,
            name: str,
            default: Optional[ParameterValueProvider] = None,
            choices: Optional[ChoicesValueProvider] = None
    ):
        self.id = id
        self.name = name
        self.default = default
        self.choices = choices

    def get_entries(self, query: str) -> List[Entry]:
        entries = self._parse_entries(query)
        if self.choices is not None:
            entries = [e for e in entries if self.choices.is_entry_in(e.value)]
        return entries

    @abstractmethod
    def _parse_entries(self, query: str) -> List[Entry]:
        pass

    @staticmethod
    def _get_entries_from_mapping(query: str, mapping: Dict[str, Any]) -> List[Entry]:
        entries = []
        for key, value in mapping.items():
            entries.extend([Entry(
                starts_from=m.start(),
                ends_at=m.end(),
                value=value() if callable(value) else value
            ) for m in re.finditer(key, query)])
        return entries


class DigitParameter(Parameter):
    REGEX = r'\b-?\d\b'
    mapper_function = int

    numbers_mapping = {
        "zero": 0,
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10
    }

    @staticmethod
    def _spawn_negative_mapping(mapping: dict) -> dict:
        new_mapping_items = list(mapping.items())
        prefixes = ["negative", "minus"]
        for key, value in mapping.items():
            for prefix in prefixes:
                new_mapping_items.append((
                    prefix + '\\s+' + key, -1 * value
                ))
        return dict(new_mapping_items)

    def _parse_entries(self, query: str) -> List[Entry]:
        entries = [Entry(
            starts_from=m.start(),
            ends_at=m.end(),
            value=self.mapper_function(m.group())
        ) for m in re.finditer(self.REGEX, query)]

        entries.extend(
            self._get_entries_from_mapping(query, self._spawn_negative_mapping(self.numbers_mapping))
        )
        return entries


class OrdinalParameter(Parameter):
    numbers_mapping = {
        "1st": 1,
        "first": 1,
        "2nd": 2,
        "second": 2,
        "3rd": 3,
        "third": 3,
        "fourth": 4,
        "fifth": 5,
        "sixth": 6,
        "seventh": 7,
        "eighth": 8,
        "ninth": 9,
        "tenth": 10
    }

    def _parse_entries(self, query: str) -> List[Entry]:
        entries = [Entry(
            starts_from=m.start(),
            ends_at=m.end(),
            value=int(m.group(1))
        ) for m in re.finditer(r'\b(\d+)-?th', query)]

        entries.extend(self._get_entries_from_mapping(query, self.numbers_mapping))
        return entries


class BooleanParameter(Parameter):
    """Check if flag present in text"""
    default = ConstantParameterValueProvider(value=False)

    def __init__(
            self,
            id: str,
            name: str
    ):
        super(BooleanParameter, self).__init__(id, name)

    def _parse_entries(self, query: str) -> List[Entry]:
        return [Entry(
            starts_from=m.start(),
            ends_at=m.end(),
            value=True
        ) for m in re.finditer(self.name, query)]


class IntegerParameter(DigitParameter):
    min_value: int
    max_value: int

    def __init__(
            self,
            id: str,
            name: str,
            default: Optional[ParameterValueProvider] = None,
            choices: Optional[ChoicesValueProvider] = None,
            min_value: int = None,
            max_value: int = None
    ):
        super(IntegerParameter, self).__init__(id, name, default, choices)
        self.min_value = min_value
        self.max_value = max_value

    REGEX = r'(-?\d+)\b'

    numbers_mapping = {
        **DigitParameter.numbers_mapping,
        "eleven": 11,
        "twelve": 12,
        "thirteen": 13,
        "fourteen": 14,
        "fifteen": 15
    }

    def _parse_entries(self, query: str) -> List[Entry]:
        entries = super(IntegerParameter, self)._parse_entries(query)
        filtered_entries = []
        for entry in entries:
            if self.max_value is not None and entry.value < self.min_value:
                continue
            elif self.max_value is not None and entry.value > self.max_value:
                continue
            filtered_entries.append(entry)
        return filtered_entries


class FloatParameter(IntegerParameter):
    REGEX = r'(-?\d*\.?\d+)\b'
    mapper_function = float


class DateParameter(Parameter):  # TODO: different date formats, related dates (2 days ago, etc)

    ISO_DATE_REGEX = r'\d{4}-\d{2}-\d{2}'

    dates_mapping = {
        "today": lambda: date.today(),
        "yesterday": lambda: date.today() - timedelta(days=1),
        "tomorrow": lambda: date.today() + timedelta(days=1),
        "now": lambda: date.today(),
        "previous day": lambda: date.today() - timedelta(days=1),
        "next day after today": lambda: date.today() + timedelta(days=1),
        "next day after tomorrow": lambda: date.today() + timedelta(days=2),
    }

    def _parse_entries(self, query: str) -> List[Entry]:

        entries = []

        entry_iso_candidates = [Entry(
            starts_from=m.start(),
            ends_at=m.end(),
            value=m.group()
        ) for m in re.finditer(self.ISO_DATE_REGEX, query)]

        for entry in entry_iso_candidates:
            try:
                entries.append(Entry(
                    starts_from=entry.starts_from,
                    ends_at=entry.ends_at,
                    value=date.fromisoformat(entry.value)
                ))
            except Exception:
                pass

        entries.extend(self._get_entries_from_mapping(query, self.dates_mapping))
        return entries


class TimeUnitParameter(Parameter):
    HOUR_UNIT = 'hour'
    MINUTE_UNIT = 'minute'
    SECOND_UNIT = 'second'

    SECONDS_IN_HOUR = 3600
    SECONDS_IN_MINUTE = 60

    MAX_DISTANCE_BETWEEN_UNITS_TO_JOIN_IN_WORDS = 2

    numbers_mapping = {
        **IntegerParameter.numbers_mapping,
        "an": 1,
        "a": 1
    }

    def get_number(self, value: str) -> int:
        if value in self.numbers_mapping:
            return self.numbers_mapping[value]

        return int(value)

    @staticmethod
    def create_regex(numbers_mapping: dict, unit: str) -> str:
        return "(\\d+|" + "|".join(numbers_mapping.keys()) + ") " + unit

    def _parse_entries(self, query: str) -> List[Entry]:
        entries = []

        hour_entries = [Entry(
            starts_from=m.start(),
            ends_at=m.end(),
            value=self.get_number(m.group(1)) * self.SECONDS_IN_HOUR
        ) for m in re.finditer(self.create_regex(self.numbers_mapping, self.HOUR_UNIT), query)]

        minute_entries = [Entry(
            starts_from=m.start(),
            ends_at=m.end(),
            value=self.get_number(m.group(1)) * self.SECONDS_IN_MINUTE
        ) for m in re.finditer(self.create_regex(self.numbers_mapping, self.MINUTE_UNIT), query)]

        second_entries = [Entry(
            starts_from=m.start(),
            ends_at=m.end(),
            value=self.get_number(m.group(1))
        ) for m in re.finditer(self.create_regex(self.numbers_mapping, self.SECOND_UNIT), query)]

        combinations_list = list(filter(lambda x: len(x), [hour_entries, minute_entries, second_entries]))

        if not combinations_list:
            return []

        for combination in itertools.product(*combinations_list):
            min_index = min([e.starts_from for e in combination])
            max_index = max([e.ends_at for e in combination])

            if (
                    query[min_index:max_index].count(" ") >
                    len(combination) * 2 - 1 + self.MAX_DISTANCE_BETWEEN_UNITS_TO_JOIN_IN_WORDS + 1
            ):
                continue

            entries.append(Entry(
                starts_from=min_index,
                ends_at=max_index,
                value=sum([e.value for e in combination])
            ))

        return entries


class TextParameter(Parameter):

    def __init__(self,
                 id: str,
                 name: str,
                 default: Optional[ParameterValueProvider] = None,
                 choices: Optional[ChoicesValueProvider] = None):
        super(TextParameter, self).__init__(id, name, default, choices)
        self.parse_from_residuals = choices is None

    def _parse_entries(self, query: str) -> List[Entry]:
        pass

    def get_entries(self, query: str) -> List[Entry]:
        if self.choices is None:
            return [
                Entry(starts_from=0, ends_at=len(query), value=query)
            ]

        if not self.choices.values:
            return []

        mapping = {}
        for value in self.choices.values:
            mapping[value.value.lower()] = (value.value, value.label)
            mapping[value.label.lower()] = (value.value, value.label)

        return self._get_entries_from_mapping(query, mapping)

