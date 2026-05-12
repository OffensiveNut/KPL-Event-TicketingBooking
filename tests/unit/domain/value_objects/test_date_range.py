import pytest
from datetime import date
from app.domain.value_objects.date_range import DateRange


def test_date_range_success():
    dr = DateRange(date(2025, 1, 1), date(2025, 1, 2))
    assert dr.start_date == date(2025, 1, 1)
    assert dr.end_date == date(2025, 1, 2)


def test_date_range_invalid():
    """US 1: The event cannot be created if the end date is earlier than the start date."""
    with pytest.raises(ValueError, match="End date can't be earlier than start date"):
        DateRange(date(2025, 1, 2), date(2025, 1, 1))

    # Same date is also invalid based on code implementation
    with pytest.raises(ValueError, match="End date can't be earlier than start date"):
        DateRange(date(2025, 1, 1), date(2025, 1, 1))
