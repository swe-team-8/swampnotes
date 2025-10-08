# Swampnotes — Team 8

A full-stack project with **FastAPI** (API), **Next.js** (web), and **PostgreSQL**.

> **Python:** 3.11.1 · **Node:** 20 LTS (20.18.1) · **Package Manager:** pnpm · **DB:** PostgreSQL 18

---

## Table of Contents
- [Prerequisites](#prereqs)
- [VS Code Setup](#vs-code-setup)
- [Backend Setup (API)](#backend-setup-api)
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