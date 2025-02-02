# Notes Backend

A **FastAPI**-powered backend for managing notes and AI insights. It provides CRUD endpoints to create, update, and delete notes, along with an example of how AI insights can be marked as resolved. The project uses **Poetry** for dependency management and **Alembic** for database migrations.

## Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Install Dependencies](#2-install-dependencies)
  - [3. Configure the Environment](#3-configure-the-environment)
  - [4. Database Migrations](#4-database-migrations)
  - [5. Run the Application](#5-run-the-application)
  - [6. Testing and Linting](#6-testing-and-linting)
- [API Endpoints](#api-endpoints)
- [Contributing](#contributing)
- [License](#license)

---

## Features

1. **Notes Management**  
   - Create, read, update, and delete user notes.
   - Supports tags, file attachments, and a creation/updated timestamp.

2. **AI Insights**  
   - Specialized note type (`AI_INSIGHT`).
   - Non-editable once created, with the ability to mark them as “resolved.”

3. **Database Migrations**  
   - Uses **Alembic** for version-controlled schema migrations.

4. **Validation and Schemas**  
   - **Pydantic** schemas to ensure data consistency.

5. **Async Startup**  
   - Automatically initializes the database schema on application startup.

6. **Dev Tooling**  
   - **Poetry** for package and environment management.
   - **Black** and **Flake8** for formatting/linting.
   - GitHub Actions workflows for continuous integration.

---

## Tech Stack

- **Python** 3.9+
- **FastAPI** for the web framework.
- **SQLAlchemy** for ORM and database connectivity.
- **Alembic** for migrations.
- **Poetry** for dependency management.
- **pytest** for testing.
- **GitHub Actions** for CI (lint and test).

---

## Project Structure

```
.
├── .github/workflows/       # GitHub Actions CI/CD config
├── migrations/              # Alembic migration scripts
├── notes_backend/           # Main FastAPI and database code
│   ├── crud/                # CRUD logic
│   ├── models/              # SQLAlchemy models
│   ├── routers/             # FastAPI routers (endpoints)
│   ├── schemas/             # Pydantic schemas
│   ├── services/            # Additional business-logic services (future expansion)
│   ├── database.py          # DB session and init
│   └── main.py              # Entry point for the FastAPI application
├── pyproject.toml           # Poetry configuration
├── alembic.ini              # Alembic config
├── .env.example             # Example env file
├── .flake8                  # Flake8 configuration
├── .gitignore
└── README.md                # Project documentation (this file)
```

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/notes-backend.git
cd notes-backend
```

### 2. Install Dependencies

Make sure you have [Poetry](https://python-poetry.org/docs/) installed.

```bash
poetry install --with dev
```

This command installs all main and development dependencies (Alembic, Flake8, Black, etc.).

### 3. Configure the Environment

1. Copy `.env.example` to `.env`.  
2. Update `DATABASE_URL` with your database connection string.

Example for local SQLite:
```bash
DATABASE_URL="sqlite:///./notes.db"
```

Alternatively, for PostgreSQL:
```bash
DATABASE_URL="postgresql://user:password@localhost:5432/mydatabase"
```

### 4. Database Migrations

This project uses **Alembic** for database migrations.

- **Generate a new migration** (after altering models):
  ```bash
  poetry run alembic revision --autogenerate -m "description_of_changes"
  ```
- **Apply migrations**:
  ```bash
  poetry run alembic upgrade head
  ```
- **Rollback the latest migration**:
  ```bash
  poetry run alembic downgrade -1
  ```

> For more detailed usage, see the [`migrations/README.md`](./migrations/README.md).

### 5. Run the Application

Start the FastAPI server using [Uvicorn](https://www.uvicorn.org/):
```bash
poetry run uvicorn notes_backend.main:app --host 0.0.0.0 --port 8000 --reload
```
> **Note**: Use `--reload` only for local development; it automatically reloads on code changes.

Check the API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

### 6. Testing and Linting

#### Run Tests

```bash
poetry run pytest
```

#### Lint and Code Format

- **Flake8**:
  ```bash
  poetry run flake8 .
  ```
- **Black**:
  ```bash
  poetry run black .
  ```

> The project also runs these steps automatically via **GitHub Actions** whenever you push or open a pull request on `main`.

---

## API Endpoints

**Base URL**: `/notes`

1. **Create a Note**  
   ```
   POST /notes/
   Body (JSON): { "text": "...", "type": "user_note", ... }
   ```
2. **Update a Note**  
   ```
   PUT /notes/{note_id}
   Body (JSON): { "text": "...", ... }
   ```
3. **Delete a Note**  
   ```
   DELETE /notes/{note_id}
   ```
4. **Resolve an AI Insight**  
   ```
   POST /notes/{note_id}/resolve
   ```
5. **Health Check**  
   ```
   GET /health
   Returns: { "status": "ok" }
   ```

For more details, visit the auto-generated **Swagger** UI at `/docs`.

---

## Contributing

1. **Fork** the repository and create a new feature branch.
2. **Commit** your changes, ensuring you follow the code style (run `black .` to format).
3. **Test** thoroughly: `pytest`.
4. **Open a Pull Request**. Our CI pipeline will run lint and tests automatically.

---

## License

This project is licensed under the [MIT License](LICENSE). You’re free to modify or distribute this software under the terms of the license.
