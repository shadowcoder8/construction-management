from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from typing import AsyncGenerator
import os

SQLALCHEMY_DATABASE_URL = f"sqlite+aiosqlite:///{os.path.abspath('labour_management.db')}"  # Use aiosqlite for async operations

# Create async engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create an AsyncSession
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def enable_wal_mode(db: AsyncSession):
    await db.execute(text("PRAGMA journal_mode=WAL;"))  # Enable WAL mode

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
        await enable_wal_mode(db)  # Enable WAL mode on session start
        try:
            yield db  # Yield the session for use in route handlers
            await db.commit()  # Commit changes if everything goes well
        except SQLAlchemyError as e:
            await db.rollback()  # Roll back in case of error
            print(f"Database error: {e}")  # Log the error (can be improved with logging)
            raise e  # Re-raise the exception for further handling in route handlers
        except Exception as e:
            await db.rollback()  # Roll back for any other exceptions
            print(f"Unexpected error: {e}")  # Log the error
            raise e  # Re-raise the exception for further handling in route handlers
