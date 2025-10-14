# Swampnotes — Team 8

A full-stack project with **FastAPI** (API), **Next.js** (web), and **PostgreSQL**.

> **Python:** 3.11.1 · **Node:** 20 LTS (20.18.1) · **Package Manager:** pnpm · **DB:** PostgreSQL 18

---

## Table of Contents
- [Prerequisites](#prereqs)
- [VS Code Setup](#vs-code-setup)
- [Backend Setup (API)](#backend-setup-api)
- [Environment Variables (API & Web)](#environment-variables-api--web)
- [Docker Services](#docker-services)
- [Database Migrations (Alembic)](#database-migrations-alembic)
- [Run the App (Dev)](#run-the-app-dev)
- [VSCode Extensions (Recommended)](#vscode-extensions-recommended)
- [Notes](#notes)

---

## Prereqs

- Git  
- **Node 20 LTS** (20.18.1)  
- **pnpm** (preferred) and **npm** (11.6.1)  
- **Python 3.11.1**  
- **Docker Desktop**  
- **OpenSSL**  
- **AWS CLI** (optional, will probably use this later) 
- **PostgreSQL 18**  
- (Optional) **nvm** to switch Node versions

---

## VS Code Setup

1. Open the repo in VS Code.
2. Select the virtualenv Python interpreter:
   - `Ctrl`+`Shift`+`P` → **Python: Select Interpreter**
   - Choose: `.\\apps\\api\\.venv\\Scripts\\python.exe` (or wherever your local venv’s `python.exe` lives)

---

## Backend Setup (API)

From the repo root:

~~~powershell
cd apps/api

# Create & activate a virtual environment
py -3.11 -m venv .venv
.\.venv\Scripts\activate

# Upgrade pip and install deps
python -m pip install -U pip
python -m pip install -r requirements.txt
~~~

<details>
<summary><strong>macOS equivalent (for Evan)</strong></summary>

~~~bash
cd apps/api
python3.11 -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
python -m pip install -r requirements.txt
~~~
</details>

---

## Environment Variables (API & Web)

These are **not tracked by Git**. Each dev has to create local env files. Restart your local dev servers after changes~

### Locations
- **API (FastAPI):** `apps/api/.env`
- **Web (Next.js):** `apps/web/.env.local`


### Example — `apps/api/.env` (FastAPI)
```ini
# Database
DATABASE_URL=postgresql+psycopg://postgres:admin@127.0.0.1:5432/swampnotes

# CORS (JSON format)
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]

# Object Storage (MinIO / S3-compatible)
S3_ENDPOINT_URL=http://localhost:9000
S3_ACCESS_KEY_ID=minio
S3_SECRET_ACCESS_KEY=minio12345
S3_BUCKET=swampnotes

# Auth
ALLOWED_EMAIL_DOMAINS=["ufl.edu","example.edu"]

# Optional JWKS override (e.g., Clerk dev):
# AUTH_JWKS_URL=https://<your-subdomain>.clerk.accounts.dev/.well-known/jwks.json

AUTH_ISSUER=https://strong-kiwi-62.clerk.accounts.dev
AUTH_AUDIENCE=fastapi
```

### Example — `apps/web/.env.local` (Next.js)
```ini
# API base URL
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000

# Clerk (public key is sent to browser, secret stays on the server-side)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_c3Ryb25nLWtpd2ktNjIuY2xlcmsuYWNjb3VudHMuZGV2JA
CLERK_SECRET_KEY=sk_test_TkI4DJF4ajvJunfSZdVfvGaH0xzhT3bfR5bqwuGeQc

# Clerk routes
NEXT_PUBLIC_CLERK_SIGN_IN_URL=/sign-in
NEXT_PUBLIC_CLERK_SIGN_UP_URL=/sign-up
NEXT_PUBLIC_CLERK_SIGN_IN_FORCE_REDIRECT_URL=/
NEXT_PUBLIC_CLERK_SIGN_UP_FORCE_REDIRECT_URL=/
```

### Notes & Env Variable Troubleshooting
- **Secrets:** Do not prefix server-only secrets with `NEXT_PUBLIC_` (those go to the browser)
- **Auth 401/403:** Verify `AUTH_ISSUER`, `AUTH_AUDIENCE`, and `AUTH_JWKS_URL`
- **CORS errors:** Confirm `CORS_ORIGINS` includes your web origin(s)
- **DB errors:** Make sure Docker is up and `DATABASE_URL` points to a reachable Postgres

---

## Docker Services

Boot up required containers:

> Run these from the directory containing `docker-compose.yaml` (or the relative path)

~~~bash
docker compose -f docker-compose.yaml up -d
~~~

---

## Database Migrations (Alembic)

**Create** a new migration (from `apps/api`):

~~~bash
cd apps/api
alembic revision --autogenerate -m "some title here"
~~~

**Apply** the latest migrations (from `apps/api`):

~~~bash
cd apps/api
alembic upgrade head
~~~

**Roll back** the latest step:

~~~bash
cd apps/api
alembic downgrade -1
~~~

**SEE** status/history (from `apps/api`):

~~~bash
cd apps/api
alembic current
alembic heads
alembic history -n -10
~~~

---

## Run the App (Dev)

**Terminal 1 — API**
~~~powershell
cd apps/api
uvicorn src.main:app --reload --port 8000
~~~

**Terminal 2 — Web**
~~~powershell
cd apps/web
pnpm dev
~~~

Now visit: <http://localhost:3000>  
This just shows the default Next.js page for now.

---

## VSCode Extensions (Recommended)

- ESLint  
- Prettier  
- Tailwind CSS IntelliSense  
- Python  
- Ruff  
- Even Better TOML

---

## Notes

- Make sure Docker is running before starting API/web (the DB depends on it).  
- If the API won’t start, confirm containers (Postgres) are healthy and all env vars are set.  
- PgAdmin4 is strongly recommended to provide a GUI for the db.
- The local postgres server MUST have a database named "swampnotes".
- DM me if (when) you hit any issues during setup.