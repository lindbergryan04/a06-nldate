from datetime import date

import pytest

from nldate import parse


@pytest.mark.parametrize(
    ("s", "today", "expected"),
    [
        ("today", date(2025, 12, 1), date(2025, 12, 1)),
        ("yesterday", date(2025, 12, 1), date(2025, 11, 30)),
        ("tomorrow", date(2025, 12, 1), date(2025, 12, 2)),
        ("Today", date(2025, 6, 15), date(2025, 6, 15)),
        ("TOMORROW", date(2025, 6, 15), date(2025, 6, 16)),
        ("YeStErDaY", date(2025, 6, 15), date(2025, 6, 14)),
        ("  today  ", date(2025, 6, 15), date(2025, 6, 15)),
        ("\ttomorrow\n", date(2025, 6, 15), date(2025, 6, 16)),
    ],
)
def test_keyword_basic(s: str, today: date, expected: date) -> None:
    assert parse(s, today) == expected


@pytest.mark.parametrize(
    ("s", "today", "expected"),
    [
        ("tomorrow", date(2025, 12, 31), date(2026, 1, 1)),
        ("yesterday", date(2025, 1, 1), date(2024, 12, 31)),
        ("tomorrow", date(2024, 2, 28), date(2024, 2, 29)),
        ("tomorrow", date(2024, 2, 29), date(2024, 3, 1)),
        ("yesterday", date(2024, 3, 1), date(2024, 2, 29)),
        ("tomorrow", date(2023, 2, 28), date(2023, 3, 1)),
        ("yesterday", date(2023, 3, 1), date(2023, 2, 28)),
        ("tomorrow", date(2000, 2, 28), date(2000, 2, 29)),
        ("yesterday", date(1900, 3, 1), date(1900, 2, 28)),
    ],
)
def test_keyword_boundary(s: str, today: date, expected: date) -> None:
    assert parse(s, today) == expected


def test_default_today_returns_a_date() -> None:
    result = parse("today")
    assert isinstance(result, date)
    assert abs((result - date.today()).days) <= 1


def test_default_today_tomorrow_is_one_day_ahead() -> None:
    assert (parse("tomorrow") - parse("today")).days == 1


def test_default_today_yesterday_is_one_day_behind() -> None:
    assert (parse("today") - parse("yesterday")).days == 1


def test_today_param_does_not_affect_absolute_dates() -> None:
    assert parse("December 1, 2025", today=date(2026, 6, 15)) == date(2025, 12, 1)
    assert parse("2020-03-15", today=date(2099, 1, 1)) == date(2020, 3, 15)


def test_unparseable_input_raises() -> None:
    with pytest.raises(ValueError):
        parse("this is not a date", today=date(2025, 12, 1))
