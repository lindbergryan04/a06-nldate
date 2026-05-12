from datetime import date

import pytest

from nldate import parse

SUNDAY = date(2025, 6, 15)
MONDAY = date(2025, 1, 6)
WEDNESDAY = date(2025, 1, 1)
SATURDAY = date(2025, 1, 4)


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("next Monday", date(2025, 6, 16)),
        ("next Tuesday", date(2025, 6, 17)),
        ("next Wednesday", date(2025, 6, 18)),
        ("next Thursday", date(2025, 6, 19)),
        ("next Friday", date(2025, 6, 20)),
        ("next Saturday", date(2025, 6, 21)),
        ("next Sunday", date(2025, 6, 22)),
    ],
)
def test_next_weekday_from_sunday(s: str, expected: date) -> None:
    assert parse(s, today=SUNDAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("last Monday", date(2025, 6, 9)),
        ("last Tuesday", date(2025, 6, 10)),
        ("last Wednesday", date(2025, 6, 11)),
        ("last Thursday", date(2025, 6, 12)),
        ("last Friday", date(2025, 6, 13)),
        ("last Saturday", date(2025, 6, 14)),
        ("last Sunday", date(2025, 6, 8)),
    ],
)
def test_last_weekday_from_sunday(s: str, expected: date) -> None:
    assert parse(s, today=SUNDAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("this Sunday", date(2025, 6, 15)),
        ("this Monday", date(2025, 6, 16)),
        ("this Tuesday", date(2025, 6, 17)),
        ("this Saturday", date(2025, 6, 21)),
    ],
)
def test_this_weekday_from_sunday(s: str, expected: date) -> None:
    assert parse(s, today=SUNDAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("Monday", date(2025, 6, 16)),
        ("Tuesday", date(2025, 6, 17)),
        ("Sunday", date(2025, 6, 22)),
    ],
)
def test_bare_weekday_from_sunday(s: str, expected: date) -> None:
    assert parse(s, today=SUNDAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("next Tue", date(2025, 6, 17)),
        ("next Tues", date(2025, 6, 17)),
        ("next Wed", date(2025, 6, 18)),
        ("next Thu", date(2025, 6, 19)),
        ("next Thurs", date(2025, 6, 19)),
        ("Fri", date(2025, 6, 20)),
        ("last Mon", date(2025, 6, 9)),
        ("Sat", date(2025, 6, 21)),
    ],
)
def test_weekday_abbreviations(s: str, expected: date) -> None:
    assert parse(s, today=SUNDAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("Next MONDAY", date(2025, 6, 16)),
        ("  next  tuesday  ", date(2025, 6, 17)),
        ("LAST friday", date(2025, 6, 13)),
    ],
)
def test_weekday_case_and_whitespace(s: str, expected: date) -> None:
    assert parse(s, today=SUNDAY) == expected


@pytest.mark.parametrize(
    ("today", "s", "expected"),
    [
        (MONDAY, "next Wednesday", date(2025, 1, 8)),
        (MONDAY, "this Monday", date(2025, 1, 6)),
        (MONDAY, "last Monday", date(2024, 12, 30)),
        (WEDNESDAY, "next Wednesday", date(2025, 1, 8)),
        (WEDNESDAY, "this Wednesday", date(2025, 1, 1)),
        (WEDNESDAY, "last Wednesday", date(2024, 12, 25)),
        (SATURDAY, "last Tuesday", date(2024, 12, 31)),
        (SATURDAY, "next Tuesday", date(2025, 1, 7)),
    ],
)
def test_weekday_from_various_anchors(today: date, s: str, expected: date) -> None:
    assert parse(s, today=today) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("1 week after Tuesday", date(2025, 6, 24)),
        ("2 days after next Friday", date(2025, 6, 22)),
        ("3 days before last Monday", date(2025, 6, 6)),
        ("1 day after this Monday", date(2025, 6, 17)),
    ],
)
def test_weekday_as_anchor(s: str, expected: date) -> None:
    assert parse(s, today=SUNDAY) == expected
