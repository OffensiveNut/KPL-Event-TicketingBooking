from dataclasses import dataclass


@dataclass(frozen=True)
class RefundId:
    value: str
