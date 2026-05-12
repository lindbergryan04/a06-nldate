from datetime import date

import pytest

from nldate import parse


@pytest.mark.parametrize(
    ("s", "expected"),
    [
        ("2025-12-01", date(2025, 12, 1)),
        ("2025/12/04", date(2025, 12, 4)),
        ("2025/1/1", date(2025, 1, 1)),
        ("2024/02/29", date(2024, 2, 29)),
        ("2025.12.01", date(2025, 12, 1)),
        ("12-04-2025", date(2025, 12, 4)),
        ("12.04.2025", date(2025, 12, 4)),
        ("Dec. 1, 2025", date(2025, 12, 1)),
        ("Sept. 15, 2024", date(2024, 9, 15)),
        ("Jan. 1st, 2025", date(2025, 1, 1)),
        ("1 Dec. 2025", date(2025, 12, 1)),
        ("December 1, 2025", date(2025, 12, 1)),
        ("December 1st, 2025", date(2025, 12, 1)),
        ("Dec 1, 2025", date(2025, 12, 1)),
        ("Dec 1 2025", date(2025, 12, 1)),
        ("1 December 2025", date(2025, 12, 1)),
        ("1st December 2025", date(2025, 12, 1)),
        ("12/1/2025", date(2025, 12, 1)),
        ("12/01/2025", date(2025, 12, 1)),
        ("March 5, 2024", date(2024, 3, 5)),
        ("Feb 29, 2024", date(2024, 2, 29)),
        ("January 1, 2000", date(2000, 1, 1)),
        ("july 4, 1776", date(1776, 7, 4)),
        ("  Dec  1,  2025  ", date(2025, 12, 1)),
    ],
)
def test_absolute_dates(s: str, expected: date) -> None:
    assert parse(s) == expected
