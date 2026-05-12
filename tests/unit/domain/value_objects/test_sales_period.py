import pytest
from datetime import date
from app.domain.value_objects.sales_period import SalesPeriod


def test_sales_period_success():
    sp = SalesPeriod(date(2025, 1, 1), date(2025, 1, 15))
    assert sp.start_date == date(2025, 1, 1)
    assert sp.end_date == date(2025, 1, 15)


def test_sales_period_invalid():
    """Sales period end date must be after start date."""
    with pytest.raises(ValueError, match="End date must be after start date"):
        SalesPeriod(date(2025, 1, 15), date(2025, 1, 1))

    # Same date is also invalid based on code implementation
    with pytest.raises(ValueError, match="End date must be after start date"):
        SalesPeriod(date(2025, 1, 1), date(2025, 1, 1))
