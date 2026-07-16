import pytest
from unittest.mock import AsyncMock
from datetime import date

from backend.crud import create_labour
from backend.schemas import LaborerCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

@pytest.mark.asyncio
async def test_create_labour_success():
    # Arrange
    mock_db = AsyncMock(spec=AsyncSession)

    labour_data = LaborerCreate(
        name="Test Labour",
        age=30,
        gender="Male",
        daily_wage=500.0,
        date_of_joining=date.today()
    )

    # Act
    result = await create_labour(mock_db, labour_data)

    # Assert
    assert result.name == "Test Labour"
    assert result.age == 30
    assert result.gender == "Male"
    assert result.daily_wage == 500.0

    mock_db.add.assert_called_once()
    mock_db.flush.assert_called_once()
    mock_db.commit.assert_called_once()
    mock_db.refresh.assert_called_once()

@pytest.mark.asyncio
async def test_create_labour_sqlalchemy_error():
    # Arrange
    mock_db = AsyncMock(spec=AsyncSession)
    mock_db.commit.side_effect = SQLAlchemyError("Mocked database error")
    mock_db.flush.side_effect = SQLAlchemyError("Mocked database error")

    labour_data = LaborerCreate(
        name="Test Labour",
        age=30,
        gender="Male",
        daily_wage=500.0,
        date_of_joining=date.today()
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await create_labour(mock_db, labour_data)

    assert exc_info.value.status_code == 500
    assert exc_info.value.detail == "Database error occurred"
