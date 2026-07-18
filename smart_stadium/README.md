# 🏟️ Smart Stadium AI System

A complete, production-ready **FastAPI** backend for a smart stadium platform — no login/signup, no frontend framework, no mock data. Every endpoint is backed by real business logic and a real SQLite database.

## Features / Modules

| # | Module | Description |
|---|--------|-------------|
| 1 | **AI Fan Assistant** | Keyword-matching Q&A engine over an FAQ knowledge base, with chat history logging. |
| 2 | **Stadium Navigation** | Points of interest, zones, and route/distance calculation between two points. |
| 3 | **Smart Ticket (QR Code)** | Ticket issuance with real QR code generation (base64 PNG), verification & check-in. |
| 4 | **Live Match Information** | Live score, minute, and status tracking for ongoing matches. |
| 5 | **Crowd Density Monitoring** | Zone-based occupancy tracking with automatic risk classification. |
| 6 | **Smart Parking** | Slot inventory, booking, and release with live availability. |
| 7 | **Food & Beverage** | Menu management and multi-item order placement with automatic totals. |
| 8 | **Weather Alerts** | Severity-based advisories with active/inactive lifecycle. |
| 9 | **Emergency SOS** | Emergency request intake and status tracking (open → acknowledged → resolved). |
| 10 | **Lost & Found** | Lost/found item reporting, keyword search, and claim tracking. |
| 11 | **Notifications** | Broadcast notifications with read/unread state. |
| 12 | **Seat Finder** | Seat registry with section/accessibility/occupancy filtering. |
| 13 | **Match Schedule** | Upcoming fixture listing (part of the Match module). |
| 14 | **Stadium Information** | Static info pages (hours, rules, contact) and amenities directory. |
| 15 | **Feedback** | Visitor ratings & comments with average-rating aggregation. |
| 16 | **Analytics** | Cross-module dashboard: tickets, matches, parking, food, crowd, safety, feedback. |
| 17 | **Admin APIs** | Protected (`X-Admin-Key` header) system overview, dashboard, and data reset. |
| 18 | **Health Check API** | Liveness/readiness probe including DB connectivity check. |

## Architecture

Clean, layered architecture — no business logic in route handlers:

```
app/
├── api/v1/endpoints/   # Route handlers (HTTP layer only)
├── api/v1/router.py    # Aggregates all routers
├── services/           # Business logic (one service class per module)
├── models/              # SQLAlchemy ORM models (one file per module)
├── schemas/             # Pydantic request/response schemas
├── database/            # Engine, session, table creation & seeding
├── utils/                # Exceptions, QR generation, responses, security
├── middleware/           # Global error handling & request logging
├── config/               # Settings (env vars) & logging configuration
└── main.py               # FastAPI app assembly & startup lifecycle
tests/                    # Unit, API, and integration tests (pytest)
docs/                     # Additional documentation
```

**Request flow:** `Router (HTTP/validation) → Service (business logic) → SQLAlchemy Model (persistence)`, with Pydantic schemas validating every input and shaping every output, and a single JSON response envelope (`success`, `message`, `data`) returned everywhere.

## Tech Stack

- **FastAPI** — async-ready REST framework with auto-generated OpenAPI docs
- **SQLAlchemy 2.0** — ORM, SQLite backend (swappable via `DATABASE_URL`)
- **Pydantic v2** — request/response validation
- **qrcode + Pillow** — real QR code image generation for tickets
- **pytest + pytest-cov** — unit, API, and integration test suite

## Getting Started

### 1. Install dependencies

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# edit .env if you want to change the admin key, database path, etc.
```

### 3. Run the server

```bash
uvicorn app.main:app --reload
```

On startup the app automatically creates all SQLite tables and seeds baseline reference data (sample matches, seats, parking slots, menu items, stadium info, and FAQ entries) if the database is empty.

- API base URL: `http://localhost:8000`
- Interactive docs (Swagger UI): `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health check: `http://localhost:8000/api/v1/health`

### 4. Try it

```bash
# Ask the AI Fan Assistant a question
curl -X POST http://localhost:8000/api/v1/assistant/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "how much does parking cost"}'

# List live matches
curl http://localhost:8000/api/v1/matches/live

# Admin: full dashboard (needs the X-Admin-Key header from .env)
curl http://localhost:8000/api/v1/admin/dashboard \
  -H "X-Admin-Key: admin-secret-key-change-me"
```

## Authentication Model

There is **no user login/signup** by design. Public fan-facing endpoints are open. The **Admin APIs** module (`/api/v1/admin/*`) is protected by a static `X-Admin-Key` header checked against `ADMIN_API_KEY` in your environment — simple, dependency-injected key verification without a user/session system.

## Testing

```bash
pytest
```

This runs the full suite (unit tests for utilities/services, API tests per module, and an end-to-end integration test simulating a fan's full stadium visit) and enforces a minimum 80% coverage gate (configured in `pytest.ini` / `.coveragerc`). An HTML coverage report is written to `htmlcov/index.html`.

Run a single module's tests:

```bash
pytest tests/test_tickets.py -v
```

## Design Notes

- **Standard response envelope**: every endpoint returns `{"success": bool, "message": str, "data": ...}`, including errors, via global exception handlers in `app/middleware/error_handler.py`.
- **Dependency injection**: the DB session (`get_db`) and admin auth (`verify_admin_key`) are injected via FastAPI's `Depends`, keeping route handlers thin and testable — see `tests/conftest.py` for how the test suite overrides the DB dependency with an isolated SQLite instance.
- **Real QR codes**: `app/utils/qrcode_util.py` uses the `qrcode` + `Pillow` libraries to generate an actual scannable PNG (base64-encoded) per ticket, not a placeholder string.
- **AI Fan Assistant**: `app/services/assistant_service.py` implements a genuine (non-mocked) keyword/Jaccard-similarity matching engine against the `faq_entries` table, with every query and response logged to `chat_logs` for auditability.
- **Logging & error handling**: `RequestLoggingMiddleware` logs every request with a correlation ID and timing; `register_exception_handlers` converts custom `AppException`s, Pydantic validation errors, and SQLAlchemy errors into consistent JSON responses instead of leaking stack traces.
- **PEP 8**: all modules use type hints, docstrings, and consistent naming/formatting throughout.

## Extending to Production

- Swap `DATABASE_URL` to PostgreSQL/MySQL (SQLAlchemy handles the dialect change; no code changes needed elsewhere).
- Put the app behind a reverse proxy (nginx) and run with multiple `uvicorn`/`gunicorn` workers.
- Replace the static `ADMIN_API_KEY` check with a proper secrets manager or OAuth2 client-credentials flow if admin access needs to scale beyond a single shared key.
- Add Alembic for schema migrations once the schema needs to evolve beyond `create_all`.
