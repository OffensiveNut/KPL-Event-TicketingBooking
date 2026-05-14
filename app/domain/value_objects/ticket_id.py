from dataclasses import dataclass


@dataclass(frozen=True)
class TicketId:
    value: str
