from dataclasses import dataclass

from app.domain.value_objects.event_id import EventId


@dataclass
class ViewEventSalesReportQuery:
    event_id: EventId
