"""Time helpers. MockPay shows every time in Indian Standard Time (IST).

Times are ISO 8601 text with the offset, for example
"2026-11-10T15:45:30+05:30". The date part is the IST date, which is the
date the settlement report uses.
"""

from datetime import datetime, timedelta, timezone

# India has one time zone and no daylight saving, so a fixed offset is exact.
IST = timezone(timedelta(hours=5, minutes=30), "IST")


def now() -> datetime:
    return datetime.now(IST)


def iso(moment: datetime) -> str:
    """ISO 8601 to the second: '2026-11-10T15:45:30+05:30'."""
    return moment.isoformat(timespec="seconds")


def iso_ms(moment: datetime) -> str:
    """ISO 8601 to the millisecond, for webhook attempts (retries are seconds apart)."""
    return moment.isoformat(timespec="milliseconds")
