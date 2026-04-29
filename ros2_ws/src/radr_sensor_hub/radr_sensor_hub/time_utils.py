from datetime import datetime
from zoneinfo import ZoneInfo

ET_ZONE = ZoneInfo("America/New_York")


def now_et() -> datetime:
    return datetime.now(ET_ZONE)


def iso_et_text() -> str:
    return now_et().isoformat(timespec="seconds")


def safe_et_text() -> str:
    return now_et().strftime("%Y-%m-%dT%H-%M-%S")
