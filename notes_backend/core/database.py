from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()

def get_database_url(async_=True):
    supabase_url = os.getenv("SUPABASE_URL")
    db_password = os.getenv("SUPABASE_DB_PASSWORD")
    
    if not supabase_url or not db_password:
        raise ValueError("SUPABASE_URL and SUPABASE_DB_PASSWORD must be set in .env file")
    
    # Extract project reference from Supabase URL
    project_ref = supabase_url.split("//")[1].split(".")[0]
    
    # Construct PostgreSQL connection URL
    if async_:
        return f"postgresql+asyncpg://postgres:{db_password}@db.{project_ref}.supabase.co:5432/postgres"
    return f"postgresql://postgres:{db_password}@db.{project_ref}.supabase.co:5432/postgres"

# Get database URLs
DATABASE_URL = get_database_url(async_=True)
SYNC_DATABASE_URL = get_database_url(async_=False)

# Create Base class for models
Base = declarative_base()

# Create engines
engine = create_async_engine(DATABASE_URL, echo=True)
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)

# Create session factories
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
