from dataclasses import dataclass


@dataclass(frozen=True)
class TicketCategoryId:
    value: str
