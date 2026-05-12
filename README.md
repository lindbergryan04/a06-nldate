# nldate

A small Python library that parses natural-language date strings into
`datetime.date` objects.

## Usage

```python
from datetime import date
from nldate import parse

parse("December 1, 2025")
# -> date(2025, 12, 1)

parse("next Tuesday", today=date(2025, 6, 15))
# -> date(2025, 6, 17)

parse("5 days before December 1st, 2025")
# -> date(2025, 11, 26)

parse("1 year and 2 months after yesterday", today=date(2025, 6, 15))
# -> date(2026, 8, 14)
```

If `today` is omitted, it defaults to `date.today()`.

## Supported input

- **Absolute dates**: `2025-12-01`, `December 1, 2025`, `Dec 1 2025`,
  `1 December 2025`, `12/1/2025` — with or without ordinal suffixes
  (`1st`, `2nd`, …) and commas.
- **Reference keywords**: `today`, `yesterday`, `tomorrow`, `now`.
- **Relative offsets**: `in 3 days`, `2 weeks ago`, `3 days from now`,
  `5 days before December 1, 2025`, `3 weeks after tomorrow`,
  `1 year and 2 months after yesterday`.
- **Next / last / this**: `next week`, `last month`, `next year`,
  `the day after tomorrow`.
- **Weekdays**: `Tuesday`, `next Friday`, `last Mon`, `this Sunday` —
  also as anchors (`2 days after next Friday`).

Input is case-insensitive and tolerant of extra whitespace.

## Development

```bash
uv sync
uv run pytest
uv run ruff check
uv run mypy
```
