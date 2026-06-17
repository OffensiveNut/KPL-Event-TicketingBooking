"""US 1: Event cannot be created with invalid schedule."""
from datetime import date

import pytest

from app.domain.value_objects.date_range import DateRange


class TestDateRange:
    def test_end_date_earlier_than_start_date_raises_error(self):
        with pytest.raises(ValueError, match="End date"):
            DateRange(start_date=date(2026, 7, 10), end_date=date(2026, 7, 9))

    def test_end_date_equal_to_start_date_raises_error(self):
        with pytest.raises(ValueError, match="End date"):
            DateRange(start_date=date(2026, 7, 10), end_date=date(2026, 7, 10))
