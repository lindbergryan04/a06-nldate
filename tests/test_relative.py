from datetime import date

import pytest

from nldate import parse

TODAY = date(2025, 6, 15)


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("in 1 day", date(2025, 6, 16)),
        ("in 3 days", date(2025, 6, 18)),
        ("in 2 weeks", date(2025, 6, 29)),
        ("in 1 week", date(2025, 6, 22)),
        ("in 1 month", date(2025, 7, 15)),
        ("in 6 months", date(2025, 12, 15)),
        ("in 1 year", date(2026, 6, 15)),
        ("in 5 years", date(2030, 6, 15)),
        ("in 0 days", date(2025, 6, 15)),
    ],
)
def test_in_n_units(s: str, expected: date) -> None:
    assert parse(s, today=TODAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("1 day ago", date(2025, 6, 14)),
        ("3 days ago", date(2025, 6, 12)),
        ("2 weeks ago", date(2025, 6, 1)),
        ("1 month ago", date(2025, 5, 15)),
        ("1 year ago", date(2024, 6, 15)),
        ("10 years ago", date(2015, 6, 15)),
    ],
)
def test_n_units_ago(s: str, expected: date) -> None:
    assert parse(s, today=TODAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("3 days from now", date(2025, 6, 18)),
        ("2 weeks from now", date(2025, 6, 29)),
        ("1 month from now", date(2025, 7, 15)),
        ("1 year from today", date(2026, 6, 15)),
        ("5 days from tomorrow", date(2025, 6, 21)),
    ],
)
def test_n_units_from_anchor(s: str, expected: date) -> None:
    assert parse(s, today=TODAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("5 days before December 1, 2025", date(2025, 11, 26)),
        ("5 days before December 1st, 2025", date(2025, 11, 26)),
        ("1 week before tomorrow", date(2025, 6, 9)),
        ("2 months before January 1, 2026", date(2025, 11, 1)),
        ("1 year before today", date(2024, 6, 15)),
        ("1 day before yesterday", date(2025, 6, 13)),
    ],
)
def test_n_units_before(s: str, expected: date) -> None:
    assert parse(s, today=TODAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("3 weeks after tomorrow", date(2025, 7, 7)),
        ("2 months after January 1, 2025", date(2025, 3, 1)),
        ("1 year after December 1, 2025", date(2026, 12, 1)),
        ("10 days after yesterday", date(2025, 6, 24)),
    ],
)
def test_n_units_after(s: str, expected: date) -> None:
    assert parse(s, today=TODAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("1 year and 2 months after yesterday", date(2026, 8, 14)),
        ("2 weeks and 3 days ago", date(2025, 5, 29)),
        ("1 year and 1 day after January 1, 2025", date(2026, 1, 2)),
        ("1 year, 2 months, and 3 days after January 1, 2025", date(2026, 3, 4)),
        ("3 months and 1 week before December 1, 2025", date(2025, 8, 25)),
    ],
)
def test_compound_offsets(s: str, expected: date) -> None:
    assert parse(s, today=TODAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("1 month after January 31, 2025", date(2025, 2, 28)),
        ("1 month after January 31, 2024", date(2024, 2, 29)),
        ("1 month after March 31, 2025", date(2025, 4, 30)),
        ("1 month after May 31, 2025", date(2025, 6, 30)),
        ("1 year after February 29, 2024", date(2025, 2, 28)),
    ],
)
def test_month_end_clamping(s: str, expected: date) -> None:
    assert parse(s, today=TODAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("next week", date(2025, 6, 22)),
        ("last week", date(2025, 6, 8)),
        ("next month", date(2025, 7, 15)),
        ("last month", date(2025, 5, 15)),
        ("next year", date(2026, 6, 15)),
        ("last year", date(2024, 6, 15)),
    ],
)
def test_next_last_unit(s: str, expected: date) -> None:
    assert parse(s, today=TODAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("in a day", date(2025, 6, 16)),
        ("a month ago", date(2025, 5, 15)),
        ("in a month", date(2025, 7, 15)),
    ],
)
def test_article_a(s: str, expected: date) -> None:
    assert parse(s, today=TODAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("the day after tomorrow", date(2025, 6, 17)),
        ("the day before yesterday", date(2025, 6, 13)),
    ],
)
def test_day_after_before(s: str, expected: date) -> None:
    assert parse(s, today=TODAY) == expected


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("  3 days ago  ", date(2025, 6, 12)),
        ("In   2   Weeks", date(2025, 6, 29)),
    ],
)
def test_relative_case_and_whitespace(s: str, expected: date) -> None:
    assert parse(s, today=TODAY) == expected
