# Database Migrations

This guide explains how to create, apply, and manage database migrations using **Alembic**.

## Environment Setup

1. **Set the `DATABASE_URL`**  
   Make sure the environment variable for your database connection is set. For local development, you might use a `.env` file:
   ```bash
   # .env
   DATABASE_URL="postgresql://user:password@localhost:5432/mydatabase"
   ```
   Or set it directly in your shell:
   ```bash
   export DATABASE_URL="postgresql://user:password@localhost:5432/mydatabase"
   ```

2. **Install Requirements**  
   Ensure you have `alembic` installed (and any other dependencies):
   ```bash
   poetry install --with dev
   # or
   pip install alembic
   ```
   > **Note**: In many projects, Alembic is included in the `[tool.poetry.group.dev.dependencies]` or `requirements-dev.txt`.

## Running Migrations

1. **Initialize Alembic** (if the `migrations/` directory isn’t already set up):
   ```bash
   alembic init migrations
   ```
   This creates the Alembic configuration files (`env.py`, `script.py.mako`, etc.). If your project already includes these files, you can skip this step.

2. **Create a New Migration**  
   If you’ve updated your SQLAlchemy models, you can autogenerate a new migration:
   ```bash
   alembic revision --autogenerate -m "description_of_changes"
   ```
   > **Tip**: If you see placeholders in the generated migration, you may need to tweak them manually to match your intended changes.

3. **Apply Migrations (Upgrade)**  
   To apply your latest migrations:
   ```bash
   alembic upgrade head
   ```
   You can also upgrade to a specific version by passing the revision ID:
   ```bash
   alembic upgrade <revision_id>
   ```

4. **Rollback Migrations (Downgrade)**  
   To revert the last applied migration:
   ```bash
   alembic downgrade -1
   ```
   Or revert to a specific version:
   ```bash
   alembic downgrade <revision_id>
   ```

## Offline vs. Online Migrations

- **Offline Mode** (`run_migrations_offline()`): Alembic generates SQL scripts without connecting to the database. Useful if the DB server is not reachable, or if you want to review the SQL before applying.
- **Online Mode** (`run_migrations_online()`): Alembic connects to the database directly and applies the migration in real-time.

By default, running commands like `alembic upgrade head` will use “online” mode. If you need an offline script for production or QA review, you can configure `env.py` accordingly or run:
```bash
alembic upgrade head --sql > upgrade_script.sql
```
to generate the SQL without applying it.

## Multi-Database Support

For multiple databases, you can maintain separate version directories. Update `alembic.ini` to define multiple `version_locations`. For example:
```ini
[alembic]
version_locations = migrations/main migrations/analytics
```
Each directory can maintain its own set of migrations pointing to different databases or schemas.

## Production vs. Local Environments

- **Local/Development**:  
  Just export your local `DATABASE_URL` and run Alembic commands as shown above.
- **Production**:  
  In a typical CI/CD pipeline, you might:
  1. Set the production database URL as an environment variable.
  2. Run `alembic upgrade head` as part of your deployment process.
  3. Possibly generate and review offline SQL scripts before applying them to production.

> **Always** test new migrations in a staging or development environment before applying them to production to avoid unexpected data loss or downtime.

## Further Tips
- **Commit your migrations** to version control so others on the team can pull the latest migration scripts.
- If you’re using Docker, run Alembic inside the container:
  ```bash
  docker compose exec web alembic upgrade head
  ```
- Keep migrations small and focused. This helps avoid merge conflicts and simplifies debugging.
