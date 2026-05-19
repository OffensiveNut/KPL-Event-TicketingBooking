from dataclasses import dataclass
from datetime import date

from app.domain.value_objects.event_id import EventId


@dataclass
class GetAllAvailableEventsQuery:
    start_date: date | None = None
    end_date: date | None = None
    location: str | None = None


@dataclass
class GetEventDetailsQuery:
    event_id: EventId
