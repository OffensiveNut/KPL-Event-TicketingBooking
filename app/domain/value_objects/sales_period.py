from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class SalesPeriod:
    start_date: date
    end_date: date

    def __post_init__(self):
        if self.end_date <= self.start_date:
            raise ValueError("End date must be after start date")

    def is_coming_soon(self) -> bool:
        return self.start_date > date.today()

    def is_ended(self) -> bool:
        return self.end_date < date.today()

    def is_active(self) -> bool:
        return self.start_date <= date.today() <= self.end_date
