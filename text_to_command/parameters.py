import itertools
import re
from abc import ABCMeta, abstractmethod
from datetime import date, timedelta
from enum import Enum
from typing import Optional, NamedTuple, Any, List, Dict

from .choices_value_provider import ChoicesValueProvider, \
    ChoicesValueProviderDeserializer
from .parameter_value_provider import ParameterValueProvider, ConstantParameterValueProvider, \
    ParameterValueProviderDeserializer


choices_value_provider_deserializer = ChoicesValueProviderDeserializer()
parameter_value_provider_deserializer = ParameterValueProviderDeserializer()


class ParameterType(Enum):
    DIGIT = 'DIGIT'
    ORDINAL = 'ORDINAL'
    BOOLEAN = 'BOOLEAN'  # FLAG
    INTEGER = 'INTEGER'
    FLOAT = 'FLOAT'
    DATE = 'DATE'
    TIME = 'TIME'  # skip for now
    TIMEUNIT = 'TIMEUNIT'
    WORD = 'WORD'  # skip for now
    TEXT = 'TEXT'


class Entry(NamedTuple):
    starts_from: int
    ends_at: int
    value: Any


class Parameter(metaclass=ABCMeta):
    type: ParameterType
    name: str
    description: str
    default: Optional[ParameterValueProvider]
    choices: Optional[ChoicesValueProvider]

    def __init__(
            self,
            name: str,
            description: str,
            default: Optional[ParameterValueProvider] = None,
            choices: Optional[ChoicesValueProvider] = None
    ):
        self.name = name
        self.description = description
        self.default = default
        self.choices = choices

    @abstractmethod
    def parse_entries(self, query: str) -> List[Entry]:
        pass

    @staticmethod
    def get_entries_from_mapping(query: str, mapping: Dict[str, Any]) -> List[Entry]:
        entries = []
        for key, value in mapping.items():
            entries.extend([Entry(
                starts_from=m.start(),
                ends_at=m.end(),
                value=value() if callable(value) else value
            ) for m in re.finditer(key, query)])
        return entries

    def to_dict(self):
        return dict(
            type=self.type.value,
            name=self.name,
            description=self.description,
            default=self.default.to_dict() if self.default else None,
            choices=self.choices.to_dict() if self.choices else None,
        )

    @classmethod
    def from_dict(cls, data: dict):
        if not data['name']:
            raise ValueError("Parameter name shouldn't be empty")
        if not data['description']:
            raise ValueError("Parameter description shouldn't be empty")

        class_parameters = dict(data)
        del class_parameters['type']

        if class_parameters.get('default'):
            class_parameters['default'] = parameter_value_provider_deserializer.from_dict(class_parameters['default'])

        if class_parameters.get('choices'):
            class_parameters['choices'] = choices_value_provider_deserializer.from_dict(class_parameters['choices'])

        return cls(
            **class_parameters
        )


class DigitParameter(Parameter):
    type = ParameterType.DIGIT

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

    def parse_entries(self, query: str) -> List[Entry]:
        entries = [Entry(
            starts_from=m.start(),
            ends_at=m.end(),
            value=self.mapper_function(m.group())
        ) for m in re.finditer(self.REGEX, query)]

        entries.extend(
            self.get_entries_from_mapping(query, self._spawn_negative_mapping(self.numbers_mapping))
        )
        return entries


class OrdinalParameter(Parameter):
    type = ParameterType.ORDINAL

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

    def parse_entries(self, query: str) -> List[Entry]:
        entries = [Entry(
            starts_from=m.start(),
            ends_at=m.end(),
            value=int(m.group(1))
        ) for m in re.finditer(r'\b(\d+)-?th', query)]

        entries.extend(self.get_entries_from_mapping(query, self.numbers_mapping))
        return entries


class BooleanParameter(Parameter):
    """Check if flag present in text"""
    type = ParameterType.BOOLEAN
    default = ConstantParameterValueProvider(value=False)

    def __init__(
            self,
            name: str,
            description: str,
    ):
        super(BooleanParameter, self).__init__(name, description)

    def parse_entries(self, query: str) -> List[Entry]:
        return [Entry(
            starts_from=m.start(),
            ends_at=m.end(),
            value=True
        ) for m in re.finditer(self.name, query)]

    def to_dict(self):
        data = super(BooleanParameter, self).to_dict()
        del data['default']
        del data['choices']
        return data


class IntegerParameter(DigitParameter):
    type = ParameterType.INTEGER

    min_value: int
    max_value: int

    def __init__(
            self,
            name: str,
            description: str,
            default: Optional[ParameterValueProvider] = None,
            choices: Optional[ChoicesValueProvider] = None,
            min_value: int = None,
            max_value: int = None
    ):
        super(IntegerParameter, self).__init__(name, description, default, choices)
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

    def parse_entries(self, query: str) -> List[Entry]:
        entries = super(IntegerParameter, self).parse_entries(query)
        filtered_entries = []
        for entry in entries:
            if self.max_value is not None and entry.value < self.min_value:
                continue
            elif self.max_value is not None and entry.value > self.max_value:
                continue
            filtered_entries.append(entry)
        return filtered_entries

    def to_dict(self):
        return dict(
            **super(IntegerParameter, self).to_dict(),
            min_value=self.min_value,
            max_value=self.max_value
        )

    @classmethod
    def from_dict(cls, data: dict):
        instance = super(IntegerParameter).from_dict(data)
        return cls(
            name=instance.name,
            description=instance.description,
            default=instance.default,
            choices=instance.choices,
            min_value=data.get('min_value'),
            max_value=data.get('max_value')
        )


class FloatParameter(IntegerParameter):
    type = ParameterType.FLOAT
    REGEX = r'(-?\d*\.?\d+)\b'
    mapper_function = float


class DateParameter(Parameter):  # TODO: different date formats, related dates (2 days ago, etc)

    type = ParameterType.DATE
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

    def parse_entries(self, query: str) -> List[Entry]:

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

        entries.extend(self.get_entries_from_mapping(query, self.dates_mapping))
        return entries


class TimeUnitParameter(Parameter):
    type = ParameterType.TIMEUNIT

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

    def parse_entries(self, query: str) -> List[Entry]:
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
    type = ParameterType.TEXT

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

    def parse_entries(self, query: str) -> List[Entry]:
        return [Entry(
            starts_from=0,
            ends_at=len(query),
            value=query
        )]


class ParameterDeserializer:
    mapping = {
        ParameterType.DIGIT: DigitParameter,
        ParameterType.ORDINAL: OrdinalParameter,
        ParameterType.BOOLEAN: BooleanParameter,
        ParameterType.INTEGER: IntegerParameter,
        ParameterType.DATE: DateParameter,
        ParameterType.TIMEUNIT: TimeUnitParameter,
        ParameterType.TEXT: TextParameter
    }

    def from_dict(self, data: dict) -> Parameter:
        return self.mapping[ParameterType(data['type'])].from_dict(data)
