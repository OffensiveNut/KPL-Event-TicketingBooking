from dataclasses import dataclass


@dataclass
class TicketCategoryDisabled:
    category_id: str
    event_id: str
