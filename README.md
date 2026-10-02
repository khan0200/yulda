# Yulda

All-in-one local marketplace connecting customers, drivers, delivery providers, employers, workers, businesses, and service providers across four verticals: **Taxi**, **Delivery/Cargo**, **Jobs**, and **Services**.

This repository currently contains the **foundation phase**: authentication, the design system, core layout/navigation, and the homepage. The marketplace verticals (Taxi booking, Delivery, Jobs, Services, Orders, Chat, Payments, Admin) are built incrementally on top of this base.

## Architecture

Yulda is a **modular monolith**: one FastAPI backend with clearly separated modules (auth, users, and — as they land — rides, deliveries, jobs, services, orders, payments, chat, notifications, admin), and one Vue 3 SPA frontend. This keeps the system simple to run and reason about while leaving clean seams to extract services later if the platform's scale demands it.

```
Browser (Vue 3 SPA)
      │ REST (axios) + WebSocket
      ▼
FastAPI backend (modular monolith)
      │                    │
      ▼                    ▼
  MongoDB              Redis
(durable data)   (cache, rate limits,
                  sessions, real-time state)
```

- **MongoDB** is the system of record: users, rides, deliveries, jobs, services, orders, payments, messages, etc., each in its own collection with purpose-built indexes (including `2dsphere` geospatial indexes for proximity queries).
- **Redis** holds transient/high-frequency state: refresh-token rotation, password-reset tokens, and — as later phases land — live driver locations and WebSocket presence, so MongoDB is never hammered with per-second GPS writes.
- **Object storage** is accessed through an abstraction (S3-compatible), not implemented directly against MongoDB, so photos/documents never bloat the database.

## Tech stack

**Frontend:** Vue 3, Vite, TypeScript, Vue Router, Pinia, Tailwind CSS, Axios, VueUse, Lucide icons.

**Backend:** Python, FastAPI, Pydantic v2, Motor (async MongoDB driver), Redis, JWT auth (access + rotating refresh tokens), slowapi rate limiting.

**Infrastructure:** MongoDB, Redis, Docker Compose for local development.

## Folder structure

```
yulda/
├── frontend/
│   └── src/
│       ├── components/   # common, navigation, maps, taxi, delivery, jobs, services, orders, chat, profile
│       ├── layouts/      # PublicLayout, AuthLayout, AppLayout
│       ├── pages/        # route-level views
│       ├── router/       # route table + auth guards
│       ├── stores/       # Pinia stores (authStore, ...)
│       ├── services/     # axios client + per-domain API modules
│       ├── types/        # shared TypeScript types
│       └── assets/       # global CSS / design tokens
├── backend/
│   └── app/
│       ├── api/v1/       # route handlers
│       ├── core/         # config, database, redis, security, exceptions, responses
│       ├── models/       # domain enums/constants
│       ├── schemas/      # Pydantic request/response schemas
│       ├── services/     # business logic
│       ├── repositories/ # MongoDB data access
│       ├── middleware/   # security headers, etc.
│       └── main.py
├── docker-compose.yml
└── .env.example
```

## Getting started

### Option A — Docker Compose (recommended)

```bash
cp .env.example .env
docker compose up --build
```

- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- API docs (Swagger): http://localhost:8000/docs
- Health check: http://localhost:8000/health

### Option B — Run locally

**Prerequisites:** Python 3.11+, Node 20+, a running MongoDB instance, a running Redis instance.

**Backend:**

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate   # Windows Git Bash; use .venv\Scripts\Activate.ps1 in PowerShell
pip install -r requirements.txt
cp ../.env.example ../.env      # edit MONGODB_URI / REDIS_URL if not using Docker
uvicorn app.main:app --reload --port 8000
```

**Frontend:**

```bash
cd frontend
npm install
npm run dev
```

## Environment variables

See [`.env.example`](.env.example) for the full list. Key variables:

| Variable | Purpose |
|---|---|
| `MONGODB_URI`, `MONGODB_DATABASE` | MongoDB connection |
| `REDIS_URL` | Redis connection |
| `JWT_SECRET`, `JWT_REFRESH_SECRET` | Token signing secrets — **generate strong random values in production** |
| `CORS_ORIGINS` | Comma-separated list of allowed frontend origins |
| `STORAGE_*` | S3-compatible object storage config |
| `MAPS_API_KEY` | Map provider key (provider-agnostic; swappable) |
| `VITE_API_BASE_URL`, `VITE_WS_BASE_URL` | Frontend → backend connection |

Never commit `.env`.

## Authentication

- Passwords hashed with bcrypt.
- Access tokens (JWT, short-lived) + refresh tokens (JWT, long-lived, rotated and tracked in Redis so a stolen refresh token can be invalidated).
- A user may hold multiple roles (`CUSTOMER`, `DRIVER`, `COURIER`, `EMPLOYER`, `WORKER`, `SERVICE_PROVIDER`, `BUSINESS`, `ADMIN`) — `roles` is an array, not a single enum field.
- `ADMIN` cannot be self-assigned at signup.
- Forgot/reset password issues a single-use token stored in Redis with a 1-hour TTL. Email delivery is not wired up yet — in development the reset token is logged server-side; plug in a real email provider before production use.

## API documentation

FastAPI auto-generates OpenAPI docs at `/docs` (Swagger UI) and `/redoc` while the backend is running. All endpoints are versioned under `/api/v1`.

All responses use a consistent envelope:

```json
{ "success": true, "data": { ... }, "message": "..." }
{ "success": false, "error_code": "NOT_FOUND", "message": "...", "details": null }
```

## Testing

**Backend** (uses `mongomock-motor` so no live database is required):

```bash
cd backend
source .venv/Scripts/activate
pytest -v
```

**Frontend type-check:**

```bash
cd frontend
npm run type-check
```

## Security notes

- All business-critical validation happens server-side via Pydantic schemas — frontend validation is UX only.
- Role checks are enforced per-endpoint via FastAPI dependencies (`require_roles(...)`), not inferred from the frontend.
- Security headers (`X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, `Permissions-Policy`) are applied to every response.
- Rate limiting is available via `slowapi` and should be applied to auth and other sensitive endpoints as they're built out.
- Password hashes and other internal fields are never included in API responses (`UserPublic` schema strips them).
- File uploads (once implemented) must be validated for type/size before reaching object storage.

## Production deployment

Not yet configured in this repository. At minimum, before deploying:

- Replace `JWT_SECRET` / `JWT_REFRESH_SECRET` with strong, unique secrets per environment.
- Run MongoDB and Redis as managed/clustered services rather than the Docker Compose containers.
- Point `STORAGE_*` at a real S3-compatible bucket.
- Serve the frontend as a static build (`npm run build`) behind a CDN/reverse proxy, with the backend behind HTTPS.
- Tighten `CORS_ORIGINS` to the real production origin(s).

## Roadmap

Foundation (this phase) → Taxi → Delivery/Cargo → Jobs → Services → Unified Orders → Chat → Notifications → Admin panel → Payments/Commission → tests & hardening throughout.
