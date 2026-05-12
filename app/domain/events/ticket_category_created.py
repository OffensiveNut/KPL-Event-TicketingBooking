from dataclasses import dataclass


@dataclass
class TicketCategoryCreated:
    event_id: str
    category_id: str
    name: str
