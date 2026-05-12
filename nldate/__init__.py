import calendar
import re
from datetime import date, timedelta

_MONTHS: dict[str, int] = {
    "january": 1, "jan": 1,
    "february": 2, "feb": 2,
    "march": 3, "mar": 3,
    "april": 4, "apr": 4,
    "may": 5,
    "june": 6, "jun": 6,
    "july": 7, "jul": 7,
    "august": 8, "aug": 8,
    "september": 9, "sep": 9, "sept": 9,
    "october": 10, "oct": 10,
    "november": 11, "nov": 11,
    "december": 12, "dec": 12,
}

_KEYWORD_OFFSETS: dict[str, int] = {
    "today": 0,
    "yesterday": -1,
    "tomorrow": 1,
    "now": 0,
}

_UNIT_DAYS: dict[str, int] = {"day": 1, "days": 1, "week": 7, "weeks": 7}
_UNIT_MONTHS: dict[str, int] = {"month": 1, "months": 1, "year": 12, "years": 12}

_MONTH_RE = "|".join(sorted(_MONTHS, key=len, reverse=True))
_UNIT_RE = "|".join(sorted([*_UNIT_DAYS, *_UNIT_MONTHS], key=len, reverse=True))
_ORDINAL_RE = re.compile(r"(\d+)(?:st|nd|rd|th)\b")


def _normalize(s: str) -> str:
    text = s.strip().lower()
    text = _ORDINAL_RE.sub(r"\1", text)
    text = re.sub(r"\bthe\s+", "", text)
    text = re.sub(rf"\ban?\s+(?={_UNIT_RE}\b)", "1 ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _add_months(d: date, months: int) -> date:
    total = d.year * 12 + (d.month - 1) + months
    y, m = divmod(total, 12)
    m += 1
    last_day = calendar.monthrange(y, m)[1]
    return date(y, m, min(d.day, last_day))


def _apply_offset(anchor: date, days: int, months: int, sign: int) -> date:
    shifted = _add_months(anchor, sign * months)
    return shifted + timedelta(days=sign * days)


def _parse_offset_clause(text: str) -> tuple[int, int] | None:
    parts = re.split(r"\s*,\s*and\s+|\s+and\s+|\s*,\s*", text.strip())
    total_days = 0
    total_months = 0
    for part in parts:
        m = re.fullmatch(rf"(?:(\d+)\s+)?({_UNIT_RE})", part.strip())
        if not m:
            return None
        n = int(m.group(1)) if m.group(1) else 1
        unit = m.group(2)
        if unit in _UNIT_DAYS:
            total_days += n * _UNIT_DAYS[unit]
        else:
            total_months += n * _UNIT_MONTHS[unit]
    return total_days, total_months


def _parse_keyword(text: str, today: date) -> date | None:
    offset = _KEYWORD_OFFSETS.get(text)
    if offset is None:
        return None
    return today + timedelta(days=offset)


def _resolve_anchor(text: str, today: date) -> date | None:
    text = text.strip()
    kw = _parse_keyword(text, today)
    if kw is not None:
        return kw
    return _parse_absolute(text)


def _parse_next_last(text: str, today: date) -> date | None:
    m = re.fullmatch(rf"(next|last|this)\s+({_UNIT_RE})", text)
    if not m:
        return None
    direction, unit = m.group(1), m.group(2)
    sign = -1 if direction == "last" else (0 if direction == "this" else 1)
    if unit in _UNIT_DAYS:
        return today + timedelta(days=sign * _UNIT_DAYS[unit])
    return _add_months(today, sign * _UNIT_MONTHS[unit])


def _parse_relative(text: str, today: date) -> date | None:
    result = _parse_next_last(text, today)
    if result is not None:
        return result

    m = re.fullmatch(r"in\s+(.+)", text)
    if m:
        offset = _parse_offset_clause(m.group(1))
        if offset is not None:
            return _apply_offset(today, offset[0], offset[1], 1)

    m = re.fullmatch(r"(.+)\s+ago", text)
    if m:
        offset = _parse_offset_clause(m.group(1))
        if offset is not None:
            return _apply_offset(today, offset[0], offset[1], -1)

    m = re.fullmatch(r"(.+?)\s+before\s+(.+)", text)
    if m:
        offset = _parse_offset_clause(m.group(1))
        anchor = _resolve_anchor(m.group(2), today)
        if offset is not None and anchor is not None:
            return _apply_offset(anchor, offset[0], offset[1], -1)

    m = re.fullmatch(r"(.+?)\s+(?:after|from)\s+(.+)", text)
    if m:
        offset = _parse_offset_clause(m.group(1))
        anchor = _resolve_anchor(m.group(2), today)
        if offset is not None and anchor is not None:
            return _apply_offset(anchor, offset[0], offset[1], 1)

    return None


def _parse_absolute(text: str) -> date | None:
    m = re.fullmatch(r"(\d{4})-(\d{1,2})-(\d{1,2})", text)
    if m:
        y, mo, d = (int(x) for x in m.groups())
        return date(y, mo, d)

    m = re.fullmatch(r"(\d{1,2})/(\d{1,2})/(\d{4})", text)
    if m:
        mo, d, y = (int(x) for x in m.groups())
        return date(y, mo, d)

    m = re.fullmatch(rf"({_MONTH_RE})\s+(\d{{1,2}}),?\s+(\d{{4}})", text)
    if m:
        return date(int(m.group(3)), _MONTHS[m.group(1)], int(m.group(2)))

    m = re.fullmatch(rf"(\d{{1,2}})\s+({_MONTH_RE}),?\s+(\d{{4}})", text)
    if m:
        return date(int(m.group(3)), _MONTHS[m.group(2)], int(m.group(1)))

    return None


def parse(s: str, today: date | None = None) -> date:
    if today is None:
        today = date.today()
    text = _normalize(s)

    result = _parse_keyword(text, today)
    if result is not None:
        return result

    result = _parse_relative(text, today)
    if result is not None:
        return result

    result = _parse_absolute(text)
    if result is not None:
        return result

    raise ValueError(f"could not parse date: {s!r}")
