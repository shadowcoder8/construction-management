import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
from datetime import date

from backend.database import Base
from backend.models import UnitType, Site, Material, Payment, Laborer, Attendance
from backend import crud, schemas

# Setup the async test database
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with TestingSessionLocal() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
def test_site_data():
    return schemas.SiteCreate(
        name="Test Site",
        location="123 Test Ave"
    )

@pytest.fixture
def test_material_data():
    return schemas.MaterialCreate(
        name="Cement",
        quantity=100.5,
        unit=UnitType.bag,
        site_id=1,  # Assuming a site with ID 1 exists
        arrival_date=date(2023, 10, 1),
        transport_type="Truck"
    )


@pytest.mark.asyncio
async def test_create_site(db_session: AsyncSession, test_site_data: schemas.SiteCreate):
    site = await crud.create_site(db_session, test_site_data)
    assert site.id is not None
    assert site.name == test_site_data.name
    assert site.location == test_site_data.location

@pytest.mark.asyncio
async def test_get_site(db_session: AsyncSession, test_site_data: schemas.SiteCreate):
    # First create a site
    site = await crud.create_site(db_session, test_site_data)

    # Then retrieve it
    fetched_site = await crud.get_site(db_session, site.id)
    assert fetched_site.id == site.id
    assert fetched_site.name == site.name

@pytest.mark.asyncio
async def test_get_site_not_found(db_session: AsyncSession):
    with pytest.raises(HTTPException) as exc_info:
        await crud.get_site(db_session, 9999)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Site not found"

@pytest.mark.asyncio
async def test_create_material(db_session: AsyncSession, test_site_data: schemas.SiteCreate, test_material_data: schemas.MaterialCreate):
    # Material needs an existing site
    site = await crud.create_site(db_session, test_site_data)
    test_material_data.site_id = site.id

    material = await crud.create_material(db_session, test_material_data)
    assert material.id is not None
    assert material.name == test_material_data.name
    assert material.quantity == test_material_data.quantity
    assert material.unit == test_material_data.unit
    assert material.site_id == site.id
    assert material.site_name == site.name

@pytest.mark.asyncio
async def test_create_material_site_not_found(db_session: AsyncSession, test_material_data: schemas.MaterialCreate):
    test_material_data.site_id = 9999
    with pytest.raises(HTTPException) as exc_info:
        await crud.create_material(db_session, test_material_data)
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Site not found"

@pytest.mark.asyncio
async def test_update_material(db_session: AsyncSession, test_site_data: schemas.SiteCreate, test_material_data: schemas.MaterialCreate):
    # Create site and material first
    site = await crud.create_site(db_session, test_site_data)
    test_material_data.site_id = site.id
    material = await crud.create_material(db_session, test_material_data)

    # Update data
    update_data = schemas.MaterialUpdate(
        name="Updated Cement",
        quantity=200.0,
        unit=UnitType.bag,
        site_id=site.id,
        arrival_date=date(2023, 10, 2),
        transport_type="Van"
    )

    updated_material = await crud.update_material(db_session, material.id, update_data)
    assert updated_material.id == material.id
    assert updated_material.name == "Updated Cement"
    assert updated_material.quantity == 200.0
    assert updated_material.transport_type == "Van"

@pytest.mark.asyncio
async def test_delete_material(db_session: AsyncSession, test_site_data: schemas.SiteCreate, test_material_data: schemas.MaterialCreate):
    # Create site and material
    site = await crud.create_site(db_session, test_site_data)
    test_material_data.site_id = site.id
    material = await crud.create_material(db_session, test_material_data)

    # Delete material
    deleted_material = await crud.delete_material(db_session, material.id)
    assert deleted_material is not None
    assert deleted_material.id == material.id

    # Verify it's gone
    fetched_material = await crud.get_material(db_session, material.id)
    assert fetched_material is None

@pytest.fixture
def test_laborer_data():
    return schemas.LaborerCreate(
        name="John Doe",
        age=30,
        gender="Male",
        daily_wage=500.0,
        date_of_joining=date(2023, 1, 15)
    )

@pytest.mark.asyncio
async def test_create_labor(db_session: AsyncSession, test_laborer_data: schemas.LaborerCreate):
    laborer = await crud.create_labour(db_session, test_laborer_data)
    assert laborer.id is not None
    assert laborer.name == test_laborer_data.name
    assert laborer.daily_wage == test_laborer_data.daily_wage

@pytest.mark.asyncio
async def test_get_labor(db_session: AsyncSession, test_laborer_data: schemas.LaborerCreate):
    laborer = await crud.create_labour(db_session, test_laborer_data)
    fetched_laborer = await crud.get_labour(db_session, laborer.id)
    assert fetched_laborer.id == laborer.id
    assert fetched_laborer.name == laborer.name

@pytest.mark.asyncio
async def test_create_attendance(db_session: AsyncSession, test_laborer_data: schemas.LaborerCreate):
    laborer = await crud.create_labour(db_session, test_laborer_data)

    attendance_data = schemas.AttendanceBase(
        laborer_id=laborer.id,
        laborer_name=laborer.name,
        date=date(2023, 10, 10),
        present="Yes",
        hours_worked=8.0,
        site_name="Test Site"
    )

    attendance = await crud.create_attendance(db_session, laborer.id, attendance_data)
    assert attendance.id is not None
    assert attendance.laborer_id == laborer.id
    assert attendance.hours_worked == 8.0

@pytest.fixture
def test_payment_data():
    return schemas.PaymentCreate(
        amount=1000.0,
        date=date(2023, 10, 15),
        labor_id=1, # Replaced dynamically
        site_id=1,  # Replaced dynamically
        description="Weekly wage"
    )

@pytest.mark.asyncio
async def test_create_payment(
    db_session: AsyncSession,
    test_laborer_data: schemas.LaborerCreate,
    test_site_data: schemas.SiteCreate,
    test_payment_data: schemas.PaymentCreate
):
    laborer = await crud.create_labour(db_session, test_laborer_data)
    site = await crud.create_site(db_session, test_site_data)

    test_payment_data.labor_id = laborer.id
    test_payment_data.site_id = site.id

    payment = await crud.create_payment(db_session, test_payment_data)
    assert payment.id is not None
    assert payment.amount == test_payment_data.amount
    assert payment.labor_id == laborer.id
    assert payment.site_id == site.id
