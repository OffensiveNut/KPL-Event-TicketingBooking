from dataclasses import dataclass


@dataclass(frozen=True)
class TicketCode:
    value: str
