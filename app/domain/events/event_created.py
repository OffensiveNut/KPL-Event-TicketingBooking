from dataclasses import dataclass


@dataclass
class EventCreated:
    event_id: str
    event_name: str
