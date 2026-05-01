from datetime import datetime


def to_iso_string(value: datetime | None) -> str:
    if value is None:
        return ""

    return value.isoformat()
