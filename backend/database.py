from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from typing import AsyncGenerator

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./labour_management.db"  # Use aiosqlite for async operations

# Create async engine
engine = create_async_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create an AsyncSession
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as db:
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
