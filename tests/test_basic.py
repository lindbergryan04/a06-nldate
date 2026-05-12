from nldate import parse


def test_parse_is_importable() -> None:
    assert callable(parse)
