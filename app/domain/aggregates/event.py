import uuid
from datetime import date

from app.domain.value_objects.date_range import DateRange
from app.domain.value_objects.event_status import EventStatus


class Event:
    def __init__(
        self,
        event_name: str,
        description: str,
        start_date: date,
        end_date: date,
        location: str,
        max_capacity: int,
    ) -> None:
        if max_capacity <= 0:
            raise ValueError("Max capacity must be greater than zero")

        self.id = str(uuid.uuid4())
        self.name = event_name
        self.description = description
        self.date = DateRange(start_date, end_date)
        self.location = location
        self.max_capacity = max_capacity
        self.status = EventStatus.DRAFT

        self._domain_events: list = []
        self._domain_events.append
