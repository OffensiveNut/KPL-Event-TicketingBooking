from dataclasses import dataclass


@dataclass(frozen=True)
class UserId:
    value: str
