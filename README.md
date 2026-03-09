# Event Management API

A robust, production-ready REST API built with **FastAPI** for managing events and participant registrations. This project demonstrates clean architecture, comprehensive testing, and best practices in Python web development.

---

## 📋 Table of Contents

- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Application](#-running-the-application)
- [Running Tests](#-running-tests)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Data Validation](#-data-validation)
- [Error Handling](#-error-handling)
- [Usage Examples](#-usage-examples)
- [Development](#-development)
- [Testing Strategy](#-testing-strategy)
- [API Documentation](#-api-documentation)
- [Deployment](#-deployment)

---

## ✨ Features

### Core Functionality
- ✅ **Event Management**: Create, read, update, and delete events
- ✅ **Participant Registration**: Register users for events with validation
- ✅ **Capacity Management**: Enforce event capacity limits
- ✅ **Duplicate Prevention**: Prevent same user registering twice for same event
- ✅ **SQLite Database**: Lightweight, file-based database with ORM support
- ✅ **Data Validation**: Pydantic models with custom validators
- ✅ **Error Handling**: Comprehensive HTTP exception handling
- ✅ **RESTful API**: Follows REST principles and conventions

### Quality Assurance
- ✅ **Comprehensive Testing**: 50+ test cases covering all endpoints and scenarios
- ✅ **Test Coverage**: Unit, integration, and edge case testing
- ✅ **Model Validation**: Tests for ORM models and Pydantic schemas
- ✅ **Capacity Testing**: Dedicated tests for capacity enforcement
- ✅ **Error Scenario Testing**: Invalid input and edge case coverage

### Developer Experience
- ✅ **Auto-Generated Documentation**: Swagger UI and ReDoc at `/docs`
- ✅ **Clean Code Architecture**: Separation of concerns (models, schemas, crud, routers)
- ✅ **Type Hints**: Full type annotation support
- ✅ **Environment Configuration**: Support for `.env` files
- ✅ **Database Migrations**: Alembic support for schema versioning

---

## 🛠 Technology Stack

### Backend Framework
- **FastAPI** (0.135.1) - Modern, fast web framework with automatic API documentation
- **Uvicorn** (0.41.0) - ASGI server for running FastAPI applications

### Database & ORM
- **SQLite** - Lightweight relational database (configurable)
- **SQLAlchemy** (2.0.48) - Python ORM with relationship support
- **Alembic** (1.18.4) - Database migration tool

### Data Validation
- **Pydantic** (2.12.5) - Data validation using Python type hints
- **Email Validation** - Built-in email format validation

### Configuration
- **python-dotenv** (1.2.2) - Load environment variables from `.env` files

### Testing
- **pytest** (7.4.4) - Testing framework
- **pytest-cov** (4.1.0) - Code coverage reporting
- **httpx** (0.25.2) - Async HTTP client for testing

---

## 📁 Project Structure

```
event-management-api/
├── app/                          # Application package
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # FastAPI application entry point
│   ├── database.py              # Database configuration and session management
│   ├── models.py                # SQLAlchemy ORM models
│   ├── schemas.py               # Pydantic validation models
│   ├── crud.py                  # Create, Read, Update, Delete operations
│   └── routers/                 # API route handlers
│       ├── __init__.py
│       ├── events.py            # Event endpoints (CRUD)
│       └── participants.py      # Participant endpoints (registration)
│
├── tests/                        # Test suite directory
│   ├── __init__.py
│   ├── conftest.py              # pytest fixtures and configuration
│   ├── test_events.py           # Event endpoint tests (50+ test cases)
│   ├── test_participants.py     # Participant endpoint tests (40+ test cases)
│   └── test_models.py           # ORM model and schema validation tests
│
├── event_management.db          # SQLite database file (auto-created)
├── .env                         # Environment variables (optional)
├── .gitignore                   # Git ignore configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

---

## 📦 Installation

### Prerequisites
- **Python 3.8+** (tested with Python 3.10+)
- **pip** or **poetry** for package management

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Anupam-Vishwakarma/event-management-api.git
   cd event-management-api
   ```

2. **Create a virtual environment**
   ```bash
   # Using venv
   python -m venv venv
   
   # Activate virtual environment
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file (optional)**
   ```bash
   # .env
   DATABASE_URL=sqlite:///./event_management.db
   ```

---

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | `sqlite:///./event_management.db` | Database connection string |

### Database Configuration

The application uses SQLite by default, but you can configure other databases:

```python
# PostgreSQL example
DATABASE_URL=postgresql://user:password@localhost:5432/events_db

# MySQL example
DATABASE_URL=mysql+pymysql://user:password@localhost:3306/events_db
```

---

## 🚀 Running the Application

### Development Mode
```bash
# Run with hot reload (auto-restart on code changes)
uvicorn app.main:app --reload

# Specify custom host and port
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production Mode
```bash
# Run without hot reload
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Access the Application
- **API Base URL**: `http://localhost:8000`
- **Interactive API Docs**: `http://localhost:8000/docs` (Swagger UI)
- **Alternative API Docs**: `http://localhost:8000/redoc` (ReDoc)
- **Health Check**: `http://localhost:8000/` (returns JSON message)

---

## 🧪 Running Tests

### Install Test Dependencies
```bash
pip install -r requirements.txt  # Already includes pytest
```

### Run All Tests
```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with output to console
pytest -s
```

### Run Specific Test Files
```bash
# Test events endpoints only
pytest tests/test_events.py -v

# Test participants endpoints only
pytest tests/test_participants.py -v

# Test models and schemas only
pytest tests/test_models.py -v
```

### Run Specific Test Classes
```bash
# Test event creation only
pytest tests/test_events.py::TestCreateEvent -v

# Test participant registration only
pytest tests/test_participants.py::TestRegisterParticipant -v
```

### Run with Code Coverage
```bash
# Generate coverage report
pytest --cov=app --cov-report=html

# View coverage report
open htmlcov/index.html  # macOS
# or
start htmlcov\index.html  # Windows
```

### Test Statistics
- **Total Test Cases**: 130+
- **Event Tests**: 50+ (creation, retrieval, updates, deletion, validation)
- **Participant Tests**: 40+ (registration, capacity, duplicates, validation)
- **Model Tests**: 40+ (schema validation, ORM relationships)

---

## 📡 API Endpoints

### Event Endpoints

#### Create Event
```http
POST /events
Content-Type: application/json

{
  "title": "Python Conference 2026",
  "description": "Annual Python conference",
  "location": "San Francisco, CA",
  "start_time": "2026-04-15T09:00:00Z",
  "end_time": "2026-04-15T17:00:00Z",
  "max_capacity": 500
}
```

**Response**: `201 Created`
```json
{
  "id": 1,
  "title": "Python Conference 2026",
  "description": "Annual Python conference",
  "location": "San Francisco, CA",
  "start_time": "2026-04-15T09:00:00Z",
  "end_time": "2026-04-15T17:00:00Z",
  "max_capacity": 500,
  "created_at": "2026-03-10T10:30:00Z",
  "updated_at": "2026-03-10T10:30:00Z"
}
```

#### Get All Events
```http
GET /events
```

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "title": "Python Conference 2026",
    ...
  },
  {
    "id": 2,
    "title": "JavaScript Meetup",
    ...
  }
]
```

#### Get Single Event
```http
GET /events/1
```

**Response**: `200 OK` (returns full event object)

**Error Response**: `404 Not Found`
```json
{
  "detail": "Event with id 999 not found"
}
```

#### Update Event
```http
PUT /events/1
Content-Type: application/json

{
  "title": "Updated Conference Title",
  "max_capacity": 600
}
```

**Response**: `200 OK` (returns updated event)

**Note**: All fields are optional. Only provided fields are updated (partial updates supported).

#### Delete Event
```http
DELETE /events/1
```

**Response**: `200 OK`
```json
{
  "message": "Event 1 deleted successfully"
}
```

---

### Participant Endpoints

#### Register for Event
```http
POST /events/1/register
Content-Type: application/json

{
  "name": "John Doe",
  "email": "john@example.com"
}
```

**Response**: `201 Created`
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "event_id": 1,
  "registered_at": "2026-03-10T10:45:00Z"
}
```

**Error: Capacity Full**
```json
{
  "detail": "Event has reached maximum capacity"
}
```

**Error: Duplicate Registration**
```json
{
  "detail": "This email is already registered for this event"
}
```

#### Get Event Participants
```http
GET /events/1/participants
```

**Response**: `200 OK`
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "event_id": 1,
    "registered_at": "2026-03-10T10:45:00Z"
  },
  {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "event_id": 1,
    "registered_at": "2026-03-10T11:00:00Z"
  }
]
```

---

## 🗄️ Database Schema

### Events Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique event identifier |
| `title` | VARCHAR(200) | NOT NULL | Event name |
| `description` | TEXT | NULLABLE | Detailed event description |
| `location` | VARCHAR(300) | NULLABLE | Event venue/location |
| `start_time` | DATETIME | NOT NULL | Event start timestamp |
| `end_time` | DATETIME | NOT NULL | Event end timestamp |
| `max_capacity` | INTEGER | NOT NULL | Maximum attendees allowed |
| `created_at` | DATETIME | NOT NULL, DEFAULT=now | Creation timestamp |
| `updated_at` | DATETIME | NOT NULL, DEFAULT=now | Last modification timestamp |

**Relationships**:
- One-to-Many with Participants (cascade delete enabled)

### Participants Table

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique participant identifier |
| `name` | VARCHAR(100) | NOT NULL | Participant name |
| `email` | VARCHAR(150) | NOT NULL | Email address |
| `event_id` | INTEGER | FOREIGN KEY | Reference to Event |
| `registered_at` | DATETIME | NOT NULL, DEFAULT=now | Registration timestamp |

**Relationships**:
- Many-to-One with Events

**Constraints**:
- Foreign key relationship with Events table
- Cascading delete: Deleting an event removes all its participants

---

## ✅ Data Validation

### Event Validation Rules

| Field | Rules |
|-------|-------|
| `title` | Required, non-empty string (max 200 chars) |
| `description` | Optional, text field |
| `location` | Optional, string (max 300 chars) |
| `start_time` | Required, ISO 8601 datetime |
| `end_time` | Required, must be AFTER start_time (not equal) |
| `max_capacity` | Required, integer > 0 |

### Participant Validation Rules

| Field | Rules |
|-------|-------|
| `name` | Required, non-empty string (max 100 chars) |
| `email` | Required, valid email format (RFC 5322) |

### Business Logic Validations

1. **Capacity Enforcement**: Prevents registration when event is at max capacity
2. **Duplicate Prevention**: Same email cannot register twice for same event
3. **Time Validation**: Event end_time must be after start_time
4. **Cascade Delete**: Deleting an event removes all participant registrations

---

## 🚨 Error Handling

### HTTP Status Codes

| Status | Scenario |
|--------|----------|
| `201 Created` | Resource successfully created |
| `200 OK` | Successful read/update/delete |
| `400 Bad Request` | Capacity full, duplicate registration, business logic violation |
| `404 Not Found` | Event or participant not found |
| `422 Unprocessable Entity` | Validation error (invalid data format/type) |
| `500 Internal Server Error` | Unexpected server error |

### Error Response Format

```json
{
  "detail": "Descriptive error message explaining the issue"
}
```

### Common Error Scenarios

```bash
# Event not found
GET /events/999
→ 404 Not Found: "Event with id 999 not found"

# Invalid capacity
POST /events
{"title": "Event", "max_capacity": 0, ...}
→ 422 Unprocessable Entity: Validation error

# Capacity exceeded
POST /events/1/register
{"name": "John", "email": "john@test.com"}
→ 400 Bad Request: "Event has reached maximum capacity"

# Duplicate registration
POST /events/1/register
{"name": "John", "email": "existing@test.com"}
→ 400 Bad Request: "This email is already registered for this event"
```

---

## 📝 Usage Examples

### Complete Workflow Example

```bash
# 1. Create an event
curl -X POST "http://localhost:8000/events/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "FastAPI Workshop",
    "description": "Learn FastAPI fundamentals",
    "location": "New York, NY",
    "start_time": "2026-04-01T09:00:00Z",
    "end_time": "2026-04-01T17:00:00Z",
    "max_capacity": 30
  }'
# Response: Event ID 1 created

# 2. Register participants
curl -X POST "http://localhost:8000/events/1/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com"
  }'

curl -X POST "http://localhost:8000/events/1/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bob Smith",
    "email": "bob@example.com"
  }'

# 3. Get all events
curl "http://localhost:8000/events/"

# 4. Get event details
curl "http://localhost:8000/events/1"

# 5. Get event participants
curl "http://localhost:8000/events/1/participants"

# 6. Update event
curl -X PUT "http://localhost:8000/events/1" \
  -H "Content-Type: application/json" \
  -d '{"max_capacity": 50}'

# 7. Delete event
curl -X DELETE "http://localhost:8000/events/1"
```

### Python Example with httpx

```python
import httpx
from datetime import datetime, timedelta, timezone

BASE_URL = "http://localhost:8000"
client = httpx.Client()

# Create event
start = datetime.now(timezone.utc) + timedelta(days=7)
end = start + timedelta(hours=8)

response = client.post(f"{BASE_URL}/events/", json={
    "title": "FastAPI Workshop",
    "start_time": start.isoformat(),
    "end_time": end.isoformat(),
    "max_capacity": 50
})
event = response.json()
event_id = event["id"]

# Register participants
for i in range(3):
    client.post(f"{BASE_URL}/events/{event_id}/register", json={
        "name": f"Participant {i+1}",
        "email": f"participant{i+1}@example.com"
    })

# Get participants
response = client.get(f"{BASE_URL}/events/{event_id}/participants")
participants = response.json()
print(f"Total participants: {len(participants)}")
```

---

## 🔧 Development

### Code Style

The project follows Python best practices:
- **Type Hints**: Full type annotation for better IDE support
- **Docstrings**: Function and class documentation
- **PEP 8**: Code formatting and naming conventions
- **Clean Architecture**: Separation of concerns

### Project Organization

```
app/
├── main.py          # Application factory and configuration
├── models.py        # Database schemas (SQLAlchemy)
├── schemas.py       # Request/response validation (Pydantic)
├── crud.py          # Business logic (Create, Read, Update, Delete)
├── database.py      # Database configuration
└── routers/         # API endpoint handlers
    ├── events.py    # Event routes
    └── participants.py  # Participant routes
```

### Adding New Features

1. **Update Models** (`app/models.py`): Define database schema
2. **Create Schemas** (`app/schemas.py`): Pydantic validation models
3. **Add CRUD Logic** (`app/crud.py`): Database operations
4. **Create Routes** (`app/routers/`): API endpoints
5. **Write Tests** (`tests/`): Test your implementation

---

## 🧪 Testing Strategy

### Test Coverage

The test suite provides comprehensive coverage:

#### Unit Tests
- Individual function/method testing
- Schema validation tests
- Model tests

#### Integration Tests
- Full endpoint workflows
- Database integration
- Error handling scenarios

#### Edge Cases
- Boundary value testing (capacity limits)
- Invalid input handling
- Duplicate prevention
- Cascade operations

### Test Organization

```
tests/
├── conftest.py           # Fixtures and test configuration
├── test_events.py        # Event endpoint tests (50+ cases)
├── test_participants.py  # Participant endpoint tests (40+ cases)
└── test_models.py        # Schema and model tests (40+ cases)
```

### Key Test Classes

| Test Class | Scenarios | Count |
|-----------|-----------|-------|
| `TestCreateEvent` | Creation, validation, errors | 12 |
| `TestGetAllEvents` | Retrieval, filtering, schema | 5 |
| `TestGetEventById` | Single retrieval, not found, errors | 5 |
| `TestUpdateEvent` | Partial/full updates, validation | 7 |
| `TestDeleteEvent` | Deletion, idempotency, cleanup | 5 |
| `TestRegisterParticipant` | Registration, capacity, duplicates | 12 |
| `TestGetEventParticipants` | Retrieval, filtering, isolation | 12 |
| `TestCapacityManagement` | Edge cases, limits | 3 |
| `TestEventIntegration` | End-to-end workflows | 3 |
| `TestEventSchema` | Pydantic validation | 12 |
| `TestParticipantSchema` | Pydantic validation | 9 |
| `TestEventModel` | ORM relationships | 2 |
| `TestParticipantModel` | ORM relationships | 2 |

---

## 📚 API Documentation

### Auto-Generated Documentation

Once the application is running, visit:

- **Swagger UI**: `http://localhost:8000/docs`
  - Interactive API documentation
  - Try out endpoints directly from browser
  - Real-time request/response examples

- **ReDoc**: `http://localhost:8000/redoc`
  - Beautiful, alternative API documentation
  - Organized by resources and operations

### Documentation Features

- **Schemas**: Automatic request/response schema documentation
- **Type Information**: Parameter types and validation rules
- **Examples**: Sample requests and responses
- **Error Codes**: Documented HTTP status codes

---

## 🚀 Deployment

### Pre-Deployment Checklist

- [ ] All tests passing (`pytest`)
- [ ] No security vulnerabilities in dependencies
- [ ] Environment variables configured
- [ ] Database backups in place
- [ ] Logging configured
- [ ] Error monitoring set up

### Deployment Options

#### Option 1: Docker (Recommended)
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Option 2: Heroku
```bash
heroku create your-app-name
git push heroku main
```

#### Option 3: AWS/Azure/GCP
Deploy as containerized service with managed PostgreSQL database.

### Production Configuration

```bash
# Environment variables for production
DATABASE_URL=postgresql://user:pass@prod-db:5432/events
WORKERS=4
DEBUG=false
```

---

## 📄 License

This project is open source and available under the MIT License.

---

## 👤 Author

**Anupam Vishwakarma**
- GitHub: [@Anupam-Vishwakarma](https://github.com/Anupam-Vishwakarma)
- Repository: [event-management-api](https://github.com/Anupam-Vishwakarma/event-management-api)

---

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Open a Pull Request

---

## ❓ FAQ

**Q: How do I change the database?**
A: Update the `DATABASE_URL` environment variable in `.env` or `app/database.py`.

**Q: Can I use this in production?**
A: Yes! The code includes proper error handling, validation, and security practices. Use a production database (PostgreSQL recommended) and ASGI server with multiple workers.

**Q: How do I add more fields to events?**
A: Add the field to the Event model in `models.py`, create a migration with Alembic, and update the schemas in `schemas.py`.

**Q: What happens when I delete an event?**
A: All participants registered for that event are automatically deleted (cascade delete).

**Q: Can multiple people use same email?**
A: No, the same email cannot register twice for the same event. Different events allow same email.

---

## 📞 Support

For issues, questions, or suggestions:
- Open an issue on [GitHub Issues](https://github.com/Anupam-Vishwakarma/event-management-api/issues)
- Check [GitHub Discussions](https://github.com/Anupam-Vishwakarma/event-management-api/discussions)

---

**Last Updated**: March 10, 2026