from dataclasses import dataclass


@dataclass(frozen=True)
class EventOrganizerId:
    value: str
