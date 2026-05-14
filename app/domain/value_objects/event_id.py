from dataclasses import dataclass


@dataclass(frozen=True)
class EventId:
    value: str
