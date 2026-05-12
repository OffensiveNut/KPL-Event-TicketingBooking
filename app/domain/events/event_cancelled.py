from dataclasses import dataclass


@dataclass
class EventCancelled:
    event_id: str
    event_name: str
    
