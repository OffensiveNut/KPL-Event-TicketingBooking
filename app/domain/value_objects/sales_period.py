from datetime import date


class SalesPeriod:
    def __init__(self, start_date: date, end_date: date) -> None:
        if end_date <= start_date:
            raise ValueError("End date must be after start date")

        self.start_date = start_date
        self.end_date = end_date

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SalesPeriod):
            return False
        return self.start_date == other.start_date and self.end_date == other.end_date
