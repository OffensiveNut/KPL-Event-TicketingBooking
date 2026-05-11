from dataclasses import dataclass


@dataclass
class EventPublished:
    event_id: str
    event_name: str
    