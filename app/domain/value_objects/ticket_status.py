from enum import Enum


class TicketStatus(Enum):
    ACTIVE = "Active"
    CHECKED_IN = "CheckedIn"
    CANCELLED = "Cancelled"
    REFUND_REQUIRED = "RefundRequired"
