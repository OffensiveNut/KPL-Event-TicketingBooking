from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class DateRange:
    start_date: date
    end_date: date

    def __post_init__(self):
        if self.end_date <= self.start_date:
            raise ValueError("End date can't be earlier than start date")

    def is_started(self, now: date) -> bool:
        return self.start_date <= now
