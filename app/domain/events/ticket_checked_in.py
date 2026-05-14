from dataclasses import dataclass

from app.domain.value_objects.ticket_id import TicketId


@dataclass
class TicketCheckedIn:
    ticket_id: TicketId
