# Event Ticketing & Booking System

An Event Ticketing & Booking System built with **Clean Architecture** and **Domain-Driven Design (DDD)**. Built with **Python 3.12+**, **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

---

## Prerequisites

- **Python 3.12+**
- **uv** — Python package and project manager
- **PostgreSQL**
- **Git**

---

## How to run the project

**1. Clone the repository**

```bash
git clone https://github.com/OffensiveNut/KPL-Event-TicketingBooking.git
cd KPL-Event-TicketingBooking
```

**2. Install dependencies**

```bash
uv sync
```

**3. Configure PostgreSQL** (see section below)

**4. Run database migration**

```bash
uv run alembic upgrade head
```

**5. Start the FastAPI server**

```bash
uv run uvicorn app.main:app --reload
```

**6. Access API documentation**

- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

---

## How to configure PostgreSQL

**1. Create the database**

```sql
CREATE DATABASE event_ticketing_db;
```

**2. Set up environment variables**

Create a `.env` file in the project root:

```ini
# Database Connection
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_NAME=event_ticketing_db

# App Settings
DEBUG=True
```

---

## How to run database migration

```bash
# Apply all pending migrations
uv run alembic upgrade head

# Create a new migration (after model changes)
uv run alembic revision --autogenerate -m "description"

# Rollback one step
uv run alembic downgrade -1
```

---

## How to run tests

```bash
# Run all tests
uv run pytest tests/ -v

# Run by layer
uv run pytest tests/unit/domain/ -v
uv run pytest tests/unit/application/ -v
```

---

## List of implemented user stories

| US  | Title                   | Description |
|-----|-------------------------|-------------|
| US1 | Create Event            | Event Organizer creates a new event with Draft status |
| US2 | Publish Event           | Event Organizer publishes a Draft event for ticket sales |
| US3 | Cancel Event            | Event Organizer cancels a Published event |
| US4 | Create Ticket Category  | Event Organizer adds ticket categories (Regular, VIP, etc.) |
| US5 | Disable Ticket Category | Event Organizer disables a ticket category from further sales |
| US6 | View Available Events   | Customer browses published events |
| US7 | View Event Details      | Customer views event info and active ticket categories |
| US8 | Create Ticket Booking   | Customer reserves tickets with PendingPayment status |
| US9 | Calculate Booking Total | Customer sees total price including service fee |
| US10| Pay Booking             | Customer pays for booking within payment deadline |
| US11| Expire Booking          | System marks unpaid bookings as Expired |
| US12| View Purchased Tickets  | Customer views tickets with unique codes |
| US13| Check In Ticket         | Gate Officer validates ticket at event entry |
| US14| Reject Invalid Ticket   | Gate Officer rejects invalid/used/wrong-event tickets |
| US15| Request Refund          | Customer requests a refund for a paid booking |
| US16| Approve Refund          | Event Organizer approves a refund request |
| US17| Reject Refund           | Event Organizer rejects a refund request with reason |
| US18| Mark Refund Paid Out    | System Admin marks approved refund as paid out |
| US19| View Sales Report       | Event Organizer views ticket sales and revenue |
| US20| View Participants       | Event Organizer views confirmed participant list |

---

## List of implemented domain events

| Domain Event               | Raised By |
|----------------------------|-----------|
| `EventCreated`             | `Event.__init__` |
| `EventPublished`           | `Event.publish()` |
| `EventCancelled`           | `Event.cancel()` |
| `TicketCategoryCreated`    | `Event.add_ticket_category()` |
| `TicketCategoryDisabled`   | `Event.disable_ticket_category()` |
| `TicketReserved`           | `Booking.__init__` |
| `BookingPaid`              | `Booking.pay()` |
| `BookingExpired`           | `Booking.expire()` |
| `TicketCheckedIn`          | `Booking.check_in_ticket()` |
| `RefundRequested`          | `Refund.__init__` |
| `RefundApproved`           | `Refund.approve()` |
| `RefundRejected`           | `Refund.reject()` |
| `RefundPaidOut`            | `Refund.paid_out()` |

---

## List of implemented application service interfaces

| Interface              | Layer       | Methods | Infrastructure Implementation |
|------------------------|-------------|---------|-------------------------------|
| `EventRepository`      | Domain      | `save()`, `get_by_id()`, `list_published()` | `SqlAlchemyEventRepository` |
| `BookingRepository`    | Domain      | `save()`, `get_by_id()`, `get_active_by_customer_event()`, `list_by_event()`, `get_booking_by_ticket_code()` | `SqlAlchemyBookingRepository` |
| `RefundRepository`     | Domain      | `save()`, `get_by_id()`, `get_by_booking_id()` | `SqlAlchemyRefundRepository` |
| `UnitOfWork`           | Application | `commit()`, `rollback()` | `SqlAlchemyUnitOfWork` |
| `PaymentGateway`       | Application | `process_payment()` | `StubPaymentGateway` |
| `NotificationService`  | Application | `send_notification()` | `StubNotificationService` |
| `RefundPaymentService` | Application | `process_refund_payout()` | `StubRefundService` |

---

## Project structure

```
app/
├── api/                     # Presentation layer (FastAPI routes & schemas)
│   └── v1/
│       ├── routes/          # event_router, booking_router, refund_router
│       └── schemas/         # Pydantic request/response models
├── application/             # Application layer (use cases, ports)
│   ├── ports/               # Secondary port interfaces
│   └── usecases/            # Commands, queries, handlers, DTOs
├── core/                    # Config & dependency injection
├── domain/                  # Domain layer (pure Python)
│   ├── aggregates/          # Event, Booking, Refund
│   ├── entities/            # Ticket, TicketCategory
│   ├── events/              # 13 domain events
│   ├── repositories/        # Repository interfaces
│   └── value_objects/       # Money, DateRange, IDs, enums, etc.
└── infrastructure/          # Infrastructure layer (SQLAlchemy, stubs)
    ├── SQLAlchemy/
    │   ├── migrations/      # Alembic migrations
    │   ├── models/          # ORM models
    │   └── repositories/    # Repository implementations
    └── services/            # Stub implementations of external services
```

---

## Architecture

The project follows **Clean Architecture** with four layers:

- **Domain** — Core business logic with aggregates, entities, value objects, domain events, and repository interfaces. No framework dependencies.
- **Application** — Use case orchestration via commands, queries, and handlers. Defines port interfaces for external systems.
- **Infrastructure** — Implements repository interfaces (SQLAlchemy/PostgreSQL) and external service adapters (payment, notification, refund stubs).
- **Presentation** — FastAPI REST controllers and Pydantic schemas.

---

## Test cases

| # | Test | Layer |
|---|------|-------|
| 1 | Event cannot be created with invalid schedule | Domain — Value Object |
| 2 | Event cannot be created with zero or negative capacity | Domain — Aggregate |
| 3 | Event cannot be published without active ticket category | Domain — Aggregate |
| 4 | Ticket category quota cannot exceed event capacity | Domain — Aggregate |
| 5 | Booking cannot be created with zero quantity | Domain — Aggregate |
| 6 | Booking cannot be paid after payment deadline | Domain — Aggregate |
| 7 | Booking cannot be paid with incorrect payment amount | Domain — Aggregate |
| 8 | Paid booking cannot expire | Domain — Aggregate |
| 9 | Checked-in ticket cannot be checked in again | Domain — Entity |
| 10 | Refund cannot be requested if ticket already checked in | Application — Handler |
| 11 | Refund cannot be approved if not in Requested status | Domain — Aggregate |
| 12 | Rejected refund must have a rejection reason | Domain — Aggregate |
