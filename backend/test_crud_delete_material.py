import sys
import types
from unittest.mock import AsyncMock, MagicMock
import unittest
import asyncio

# Setup mock environment for backend.crud
def setup_mocks():
    if "fastapi" in sys.modules:
        return
    # Mock fastapi
    fastapi = types.ModuleType("fastapi")
    class HTTPException(Exception):
        def __init__(self, status_code, detail):
            self.status_code = status_code
            self.detail = detail
    fastapi.HTTPException = HTTPException
    sys.modules["fastapi"] = fastapi

    # Mock sqlalchemy
    sqlalchemy = types.ModuleType("sqlalchemy")
    sqlalchemy.select = lambda *args, **kwargs: None
    sqlalchemy.func = type("func", (), {})()
    sqlalchemy.update = lambda *args, **kwargs: None
    sqlalchemy.delete = lambda *args, **kwargs: None
    sqlalchemy.Column = lambda *args, **kwargs: None
    sqlalchemy.Integer = None
    sqlalchemy.String = None
    sqlalchemy.Float = None
    sqlalchemy.Date = None
    sqlalchemy.Enum = lambda *args, **kwargs: None
    sqlalchemy.ForeignKey = lambda *args, **kwargs: None
    sqlalchemy.text = lambda *args, **kwargs: None
    sys.modules["sqlalchemy"] = sqlalchemy

    # Mock sqlalchemy.exc
    sqlalchemy_exc = types.ModuleType("sqlalchemy.exc")
    class SQLAlchemyError(Exception):
        pass
    sqlalchemy_exc.SQLAlchemyError = SQLAlchemyError
    sys.modules["sqlalchemy.exc"] = sqlalchemy_exc

    # Mock sqlalchemy.ext
    sqlalchemy_ext = types.ModuleType("sqlalchemy.ext")
    sys.modules["sqlalchemy.ext"] = sqlalchemy_ext

    # Mock sqlalchemy.ext.declarative
    sqlalchemy_ext_declarative = types.ModuleType("sqlalchemy.ext.declarative")
    sqlalchemy_ext_declarative.declarative_base = lambda: type("Base", (), {})
    sys.modules["sqlalchemy.ext.declarative"] = sqlalchemy_ext_declarative

    # Mock sqlalchemy.ext.asyncio
    sqlalchemy_ext_asyncio = types.ModuleType("sqlalchemy.ext.asyncio")
    class AsyncSession:
        pass
    sqlalchemy_ext_asyncio.AsyncSession = AsyncSession
    sqlalchemy_ext_asyncio.create_async_engine = lambda *args, **kwargs: None
    sys.modules["sqlalchemy.ext.asyncio"] = sqlalchemy_ext_asyncio

    # Mock sqlalchemy.orm
    sqlalchemy_orm = types.ModuleType("sqlalchemy.orm")
    sqlalchemy_orm.selectinload = lambda *args, **kwargs: None
    sqlalchemy_orm.joinedload = lambda *args, **kwargs: None
    sqlalchemy_orm.relationship = lambda *args, **kwargs: None
    sqlalchemy_orm.declarative_base = lambda: type("Base", (), {})
    sqlalchemy_orm.mapped_column = lambda *args, **kwargs: None
    sqlalchemy_orm.Mapped = lambda *args, **kwargs: None
    sqlalchemy_orm.sessionmaker = lambda *args, **kwargs: None
    sys.modules["sqlalchemy.orm"] = sqlalchemy_orm

    # Mock passlib
    passlib = types.ModuleType("passlib")
    passlib_context = types.ModuleType("passlib.context")
    class CryptContext:
        def __init__(self, *args, **kwargs): pass
    passlib_context.CryptContext = CryptContext
    passlib.context = passlib_context
    sys.modules["passlib"] = passlib
    sys.modules["passlib.context"] = passlib_context

    # Mock pydantic
    pydantic = types.ModuleType("pydantic")
    class BaseModel:
        def __init__(self, **kwargs):
            for k, v in kwargs.items():
                setattr(self, k, v)
        def model_dump(self):
            return {}
    pydantic.BaseModel = BaseModel
    pydantic.EmailStr = str
    class Field:
        def __init__(self, *args, **kwargs): pass
    pydantic.Field = Field
    def computed_field(*args, **kwargs):
        if len(args) == 1 and callable(args[0]): return args[0]
        return lambda f: f
    pydantic.computed_field = computed_field
    sys.modules["pydantic"] = pydantic

    pydantic_config = types.ModuleType("pydantic.config")
    class ConfigDict:
        pass
    pydantic_config.ConfigDict = ConfigDict
    sys.modules["pydantic.config"] = pydantic_config

setup_mocks()

import backend.crud as crud
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

def async_test(coro):
    def wrapper(*args, **kwargs):
        return asyncio.run(coro(*args, **kwargs))
    return wrapper

class TestDeleteMaterial(unittest.TestCase):

    @async_test
    async def test_delete_material_success(self):
        db_mock = AsyncMock()
        dummy = MagicMock()
        dummy.id = 1
        dummy.name = "Cement"
        dummy.quantity = 50
        dummy.unit = "Bags"
        dummy.site_id = 1
        dummy.arrival_date = "2023-10-01"
        dummy.transport_type = "Truck"
        db_mock.get.return_value = dummy

        result = await crud.delete_material(db_mock, 1)

        db_mock.delete.assert_called_once_with(dummy)
        db_mock.commit.assert_called_once()
        self.assertEqual(result.id, 1)
        self.assertEqual(result.name, "Cement")

    @async_test
    async def test_delete_material_not_found(self):
        db_mock = AsyncMock()
        db_mock.get.return_value = None

        result = await crud.delete_material(db_mock, 999)

        db_mock.delete.assert_not_called()
        self.assertIsNone(result)

    @async_test
    async def test_delete_material_sqlalchemy_error(self):
        db_mock = AsyncMock()
        dummy = MagicMock()
        db_mock.get.return_value = dummy
        db_mock.delete.side_effect = SQLAlchemyError("mock db error")
        try:
            await crud.delete_material(db_mock, 1)
            self.fail("Should have raised exception")
        except HTTPException as e:
            self.assertEqual(e.status_code, 500)
            self.assertIn("Database error occurred", e.detail)
            db_mock.rollback.assert_called_once()

    @async_test
    async def test_delete_material_unexpected_error(self):
        db_mock = AsyncMock()
        dummy = MagicMock()
        db_mock.get.return_value = dummy
        db_mock.delete.side_effect = Exception("mock generic error")
        try:
            await crud.delete_material(db_mock, 1)
            self.fail("Should have raised exception")
        except HTTPException as e:
            self.assertEqual(e.status_code, 500)
            self.assertIn("An unexpected error occurred", e.detail)
            db_mock.rollback.assert_called_once()

if __name__ == '__main__':
    unittest.main()
