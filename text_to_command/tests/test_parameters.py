from datetime import date

import pytest

from text_to_command.choices_value_provider import ChoicesValueProvider, ChoiceValue
from text_to_command.parameters import DigitParameter, Entry, OrdinalParameter, BooleanParameter, IntegerParameter, \
    FloatParameter, DateParameter, TimeUnitParameter


class TestDigitParsing:
    parameter = DigitParameter("id", "test")
    parameter_with_choices = DigitParameter("id", "test", choices=ChoicesValueProvider(values=[
        ChoiceValue(label="1", value=1),
        ChoiceValue(label="2", value=2),
        ChoiceValue(label="3", value=3),
        ChoiceValue(label="4", value=4),
        ChoiceValue(label="5", value=5),
    ], is_lazy=False))

    @pytest.mark.parametrize("query,expected_answers", [
        ("1", {1}),
        ("2", {2}),
    ])
    def test_parse_single_digit(self, query, expected_answers):
        assert {e.value for e in self.parameter.get_entries(query)} == expected_answers

    @pytest.mark.parametrize("query,expected_answers", [
        ("1, 2, 3, 4, 5, 6, 7, 8,9, 10", {1, 2, 3, 4, 5, 6, 7, 8, 9}),
        ("1-2,3", {1, -2, 3}),
        ("1 minus one,  negative three, ,3", {1, -1, -3, 3}),
    ])
    def test_parse_multiple_digits(self, query, expected_answers):
        assert {e.value for e in self.parameter.get_entries(query)} == expected_answers

    @pytest.mark.parametrize("query,expected_answers", [
        ("1, 2, 3, 4, 5, 6, 7, 8,9, 10", {1, 2, 3, 4, 5}),
    ])
    def test_parse_multiple_digits(self, query, expected_answers):
        assert {e.value for e in self.parameter_with_choices.get_entries(query)} == expected_answers

    @pytest.mark.parametrize("query,expected_answers", [
        ("one, two", {1, 2}),
        ("two,three", {2, 3}),
    ])
    def test_parse_multiple_string_digits(self, query, expected_answers):
        assert {e.value for e in self.parameter.get_entries(query)} == expected_answers

    @pytest.mark.parametrize("query,expected_answers", [
        ("one, 2", {1, 2}),
        ("1,three", {1, 3}),
    ])
    def test_parse_multiple_mixed_digits(self, query, expected_answers):
        assert {e.value for e in self.parameter.get_entries(query)} == expected_answers

    @pytest.mark.parametrize("query,expected_answers", [
        ("one, 2", {Entry(starts_from=0, ends_at=3, value=1), Entry(starts_from=5, ends_at=6, value=2)}),
        ("1,three", {Entry(starts_from=0, ends_at=1, value=1), Entry(starts_from=2, ends_at=7, value=3)}),
    ])
    def test_parse_entries(self, query, expected_answers):
        assert set(self.parameter.get_entries(query)) == expected_answers


class TestOrdinalParsing:
    parameter = OrdinalParameter("id", "test")

    @pytest.mark.parametrize("query,expected_answers", [
        ("one, 2", set()),
        ("1,2th, 3rd", {Entry(starts_from=2, ends_at=5, value=2), Entry(starts_from=7, ends_at=10, value=3)}),
        ("first,9th", {Entry(starts_from=0, ends_at=5, value=1), Entry(starts_from=6, ends_at=9, value=9)}),
    ])
    def test_parse_entries(self, query, expected_answers):
        assert set(self.parameter.get_entries(query)) == expected_answers


class TestBooleanParameter:
    parameter = BooleanParameter("id", "test")

    @pytest.mark.parametrize("query,expected_answers", [
        ("1, ttt", set()),
        ("2th, test", {Entry(starts_from=5, ends_at=9, value=True)}),
        ("test,test", {Entry(starts_from=0, ends_at=4, value=True), Entry(starts_from=5, ends_at=9, value=True)}),
    ])
    def test_parse_entries(self, query, expected_answers):
        assert set(self.parameter.get_entries(query)) == expected_answers


class TestIntegerParameter:

    @pytest.mark.parametrize("query,expected_answers", [
        ("1, 12", {
            Entry(starts_from=0, ends_at=1, value=1),
            Entry(starts_from=3, ends_at=5, value=12)
        }),
        ("2th, 25", {Entry(starts_from=5, ends_at=7, value=25)}),
        ("-1, 1, one, negative 2, minus three", {
            Entry(starts_from=0, ends_at=2, value=-1),
            Entry(starts_from=4, ends_at=5, value=1),
            Entry(starts_from=7, ends_at=10, value=1),
            Entry(starts_from=21, ends_at=22, value=2),
            Entry(starts_from=24, ends_at=35, value=-3),
            Entry(starts_from=30, ends_at=35, value=3)
        }),
    ])
    def test_parse_entries(self, query, expected_answers):
        parameter = IntegerParameter("id", "test")
        assert set(parameter.get_entries(query)) == expected_answers

    @pytest.mark.parametrize("query,expected_answers", [
        ("-1, -5, 11, 9", {
            Entry(starts_from=0, ends_at=2, value=-1),
            Entry(starts_from=12, ends_at=13, value=9)
        }),
    ])
    def test_parse_entries_with_min_max(self, query, expected_answers):
        parameter = IntegerParameter("id", "test", min_value=-3, max_value=10)
        assert set(parameter.get_entries(query)) == expected_answers


class TestFloatParameter:

    @pytest.mark.parametrize("query,expected_answers", [
        ("-1.2, 12.5", {
            Entry(starts_from=0, ends_at=4, value=-1.2),
            Entry(starts_from=6, ends_at=10, value=12.5)
        }),
    ])
    def test_parse_entries(self, query, expected_answers):
        parameter = FloatParameter("id", "test")
        assert set(parameter.get_entries(query)) == expected_answers


class TestDateParameter:
    parameter = DateParameter("id", "test")

    @pytest.mark.parametrize("query,expected_answers", [
        ("2020-01-01, 2021-12-10", {
            Entry(starts_from=0, ends_at=10, value=date(2020, 1, 1)),
            Entry(starts_from=12, ends_at=22, value=date(2021, 12, 10)),
        }),
    ])
    def test_parse_entries(self, query, expected_answers):
        assert set(self.parameter.get_entries(query)) == expected_answers


class TestTimeUnitParameter:
    parameter = TimeUnitParameter("id", "test")

    @pytest.mark.parametrize("query,expected_answers", [
        ("1 second", {Entry(starts_from=0, ends_at=8, value=1)}),
        ("a second", {Entry(starts_from=0, ends_at=8, value=1)}),
        ("two seconds", {Entry(starts_from=0, ends_at=10, value=2)}),
        ("5 seconds", {Entry(starts_from=0, ends_at=8, value=5)}),
        ("5 minutes", {Entry(starts_from=0, ends_at=8, value=300)}),
        ("5 hours", {Entry(starts_from=0, ends_at=6, value=3600 * 5)}),
        ("5 seconds 5 minutes", {Entry(starts_from=0, ends_at=18, value=305)}),
        ("5 minutes and 5 seconds", {Entry(starts_from=0, ends_at=22, value=305)}),
    ])
    def test_parse_entries(self, query, expected_answers):
        assert set(self.parameter.get_entries(query)) == expected_answers
