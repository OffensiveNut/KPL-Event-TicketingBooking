from enum import Enum


class RefundStatus(Enum):
    REQUESTED = "Requested"
    APPROVED = "Approved"
    REJECTED = "Rejected"
    PAIDOUT = "PaidOut"
