from dataclasses import dataclass

from app.domain.value_objects.event_id import EventId


@dataclass
class EventCancelled:
    event_id: EventId
    event_name: str
