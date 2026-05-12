import re
from datetime import date, timedelta

_KEYWORD_OFFSETS: dict[str, int] = {
    "today": 0,
    "yesterday": -1,
    "tomorrow": 1,
}

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

_MONTH_RE = "|".join(sorted(_MONTHS, key=len, reverse=True))
_ORDINAL_RE = re.compile(r"(\d+)(?:st|nd|rd|th)\b")


def _normalize(s: str) -> str:
    text = s.strip().lower()
    text = _ORDINAL_RE.sub(r"\1", text)
    text = re.sub(r"\s+", " ", text)
    return text


def _parse_keyword(text: str, today: date) -> date | None:
    offset = _KEYWORD_OFFSETS.get(text)
    if offset is None:
        return None
    return today + timedelta(days=offset)


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

    result = _parse_absolute(text)
    if result is not None:
        return result

    raise ValueError(f"could not parse date: {s!r}")
