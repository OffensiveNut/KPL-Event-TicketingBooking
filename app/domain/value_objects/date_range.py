from datetime import date


class DateRange:
    def __init__(self, start_date: date, end_date: date) -> None:
        if end_date <= start_date:
            raise ValueError("End date can't be earlier than start date")

        self.start_date = start_date
        self.end_date = end_date

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DateRange):
            return False
        return self.start_date == other.start_date and self.end_date == other.end_date
