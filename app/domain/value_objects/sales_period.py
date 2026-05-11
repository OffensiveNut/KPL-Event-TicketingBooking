from datetime import date


class SalesPeriod:
    def __init__(self, start_date: date, end_date: date) -> None:
        if end_date <= start_date:
            raise ValueError("End date must be after start date")

        self.start_date = start_date
        self.end_date = end_date
