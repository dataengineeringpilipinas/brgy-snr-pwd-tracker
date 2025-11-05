"""Database configuration and initialization."""
import os
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

# Import all models so SQLModel can create tables
from app.models import Senior, PWD, Benefit, Visit, AssistanceDrive  # noqa: F401

# Determine database path
if os.path.exists("/data"):
    # Production on Fly.io - use volume
    DB_PATH = Path("/data/brgy_snr_pwd.db")
else:
    # Development - use local file
    DB_PATH = Path("./brgy_snr_pwd.db")

# Ensure directory exists
DB_PATH.parent.mkdir(parents=True, exist_ok=True)

DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=True, future=True)

# Create async session maker
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncSession:
    """Get database session."""
    async with async_session() as session:
        yield session


async def init_db() -> None:
    """Initialize database and create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

