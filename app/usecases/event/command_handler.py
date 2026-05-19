from app.domain.aggregates.event import Event
from app.domain.repositories.event_repository import EventRepository
from app.usecases.event.commands import (
    CancelEventCommand,
    CreateEventCommand,
    PublishEventCommand,
)


class CreateEventCommandHandler:
    def __init__(self, event_repository: EventRepository):
        self._event_repository = event_repository

    def handle(self, command: CreateEventCommand) -> str:
        event = Event(
            event_name=command.event_name,
            description=command.description,
            start_date=command.start_date,
            end_date=command.end_date,
            location=command.location,
            max_capacity=command.max_capacity,
            event_organizer=command.event_organizer,
        )
        self._event_repository.save(event)
        return event.id.value


class PublishEventCommandHandler:
    def __init__(self, event_repository: EventRepository):
        self._event_repository = event_repository

    def handle(self, command: PublishEventCommand) -> None:
        event = self._event_repository.get_by_id(command.event_id)
        if event is None:
            raise ValueError(f"Event with id {command.event_id} not found")
        event.publish()


class CancelEventCommandHandler:
    def __init__(self, event_repository: EventRepository):
        self._event_repository = event_repository

    def handle(self, command: CancelEventCommand) -> None:
        event = self._event_repository.get_by_id(command.event_id)
        if event is None:
            raise ValueError(f"Event with id {command.event_id} not found")
        event.cancel()
