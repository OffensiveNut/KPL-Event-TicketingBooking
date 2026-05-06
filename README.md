# Event Ticketing & Booking System

## Prerequisites

Before running this project, ensure you have the following installed on your local machine:

* **Python 3.12+**: The core programming language used for development.
* **uv**: A fast Python package and project manager used to handle the environment and dependencies.
* **PostgreSQL**: The required relational database for persisting aggregate data.
* **Git**: Essential for version control and collaborating via pair programming.

---

## How to run the project

This project utilizes `uv` to manage the virtual environment and dependencies automatically, ensuring consistency across development environments.

**1. Clone the repository**
```bash
git clone https://github.com/OffensiveNut/KPL-Event-TicketingBooking.git
cd KPL-Event-TicketingBooking
```
**2. Install dependencies**  
This command synchronizes your environment with the uv.lock file, creating a .venv and installing all required packages.

```Bash
uv sync
```
**3. Start the FastAPI server**   
Run the application using uvicorn. The --reload flag enables hot-reloading, which automatically refreshes the server when code changes are detected.

```Bash
uv run uvicorn src.main:app --reload
```
1. Access the Documentation   
FastAPI automatically generates interactive documentation in the presentation layer. Once the server is running, visit:   
    ```bash
    Swagger UI: http://127.0.0.1:8000/docs
    ReDoc: http://127.0.0.1:8000/redoc
    ```
## How to configure PostgreSQL
The system requires a running PostgreSQL instance to persist aggregate data.

**1. Create the Database**   
Access your PostgreSQL terminal (psql) or a management tool like pgAdmin and create a new database for the project:

```SQL
CREATE DATABASE event_ticketing_db;
```
2. Setup Environment Variables
Create a .env file in the root directory. This file is used by pydantic-settings to securely pass configuration to the infrastructure layer. Add your local credentials:

``` shell
# Database Connection
DB_HOST=localhost
DB_PORT=5432
DB_USER=your_postgres_username
DB_PASSWORD=your_postgres_password
DB_NAME=event_ticketing_db

# App Settings
DEBUG=True
```
3. Database Integration
The application will use these settings to implement the repository interfaces in the infrastructure layer, allowing for the persistence of aggregates such as Event, Booking, and Ticket.
## How to run database migration
## How to run tests
## List of implemented user stories
## List of implemented domain events
## List of implemented application service interfaces