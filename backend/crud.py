from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func,update, delete
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from backend import models, schemas
from sqlalchemy.orm import selectinload,joinedload
from backend.models import Attendance,Site,Material
from backend.schemas import MaterialUpdate
from typing import List,Optional
import logging

logger = logging.getLogger(__name__)


# Create Labour
async def create_labour(db: AsyncSession, labour: schemas.LaborerCreate):
    db_labour = models.Laborer(**labour.model_dump())
    db.add(db_labour)
    await db.flush()  # Flush before commit to handle potential primary key creation
    await db.commit()
    await db.refresh(db_labour)
    return db_labour

# Get All Labours
async def get_labours(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(select(models.Laborer).offset(skip).limit(limit))
    return result.scalars().all()

# Search Labours by Name
async def search_labours(db: AsyncSession, name: str):
    result = await db.execute(select(models.Laborer).filter(models.Laborer.name.ilike(f"%{name}%")))
    return result.scalars().all()

# Get a single Labour by ID
async def get_labour(db: AsyncSession, labour_id: int):
    result = await db.execute(select(models.Laborer).filter(models.Laborer.id == labour_id))
    return result.scalar_one_or_none()

# Update Labour
async def update_labour(db: AsyncSession, labour_id: int, updated_data: schemas.LaborerCreate):
    labour = await get_labour(db, labour_id)
    if labour:
        for key, value in updated_data.model_dump().items():
            setattr(labour, key, value)
        await db.commit()
        await db.refresh(labour)
        return labour
    return None

# Delete Labour
async def delete_labour(db: AsyncSession, labour_id: int):
    labour = await get_labour(db, labour_id)
    if labour:
        await db.delete(labour)
        await db.commit()
        return True
    return False

# Create Attendance Record
async def create_attendance(db: AsyncSession, labour_id: int, attendance: schemas.AttendanceBase):
    # Create a new Attendance instance
    new_attendance = models.Attendance(
        laborer_id=labour_id,
        date=attendance.date,  # Assuming date is part of the attendance object
        present=attendance.present,
        hours_worked=attendance.hours_worked,
        site_name=attendance.site_name,
    )
    
    db.add(new_attendance)
    await db.commit()
    await db.refresh(new_attendance)  # Refresh to get the newly created instance
    return new_attendance



# CRUD function to get attendance with pagination
async def get_all_attendance(db: AsyncSession, skip: int, limit: int):
    result = await db.execute(
        select(models.Attendance)
        .options(selectinload(models.Attendance.laborer))  # Assuming you have a relationship named 'laborer'
        .offset(skip)
        .limit(limit)
    )
    return [
        {
            "id": attendance.id,
            "laborer_id": attendance.laborer.id,
            "laborer_name": attendance.laborer.name,  # Access the laborer name here
            "date": attendance.date,
            "present": attendance.present,
            "hours_worked": attendance.hours_worked,
            "site_name": attendance.site_name
        }
        for attendance in result.scalars().all()
    ]


# Function to count total attendance records
async def count_all_attendance(db: AsyncSession) -> int:
    query = select(func.count()).select_from(models.Attendance)  # Count total records
    result = await db.execute(query)
    return result.scalar()  # Return the count


# Get Attendance History
async def get_attendance_history(db: AsyncSession, laborer_id: int):
    result = await db.execute(select(models.Attendance).filter(models.Attendance.laborer_id == laborer_id))
    return result.scalars().all()

# get single attendance
async def get_attendance(db: AsyncSession, attendance_id: int) -> schemas.Attendance:
    # Join Attendance with the Laborer table to get the laborer_name
    result = await db.execute(
        select(Attendance)
        .options(joinedload(Attendance.laborer))  # Assuming there's a relationship named 'laborer'
        .filter(Attendance.id == attendance_id)
    )
    attendance = result.scalar_one_or_none()

    if attendance:
        # Manually populate laborer_name for the response
        return schemas.Attendance(
            id=attendance.id,
            laborer_id=attendance.laborer_id,
            laborer_name=attendance.laborer.name,  # Add laborer_name
            date=attendance.date,
            present=attendance.present,
            hours_worked=attendance.hours_worked,
            site_name=attendance.site_name
        )
    return None  # If no attendance record is found

# Delete Attendance Record
async def delete_attendance(db: AsyncSession, attendance_id: int):
    # Fetch the attendance record by ID
    result = await db.execute(select(models.Attendance).filter(models.Attendance.id == attendance_id))
    attendance = result.scalar_one_or_none()

    if attendance:
        # If attendance record is found, delete it
        await db.delete(attendance)
        await db.commit()  # Commit the transaction
        return True

    return False  # Return False if attendance record is not found


# Update attendance function to include laborer_name
async def update_attendance(db: AsyncSession, attendance_id: int, attendance_data: schemas.AttendanceUpdate) -> schemas.Attendance:
    # Fetch the attendance record to update
    result = await db.execute(
        select(Attendance).options(joinedload(Attendance.laborer)).filter(Attendance.id == attendance_id)
    )
    attendance = result.scalar_one_or_none()

    if attendance is None:
        return None  # Return None if the attendance record does not exist

    # Update the attendance record fields
    if attendance_data.present is not None:
        attendance.present = attendance_data.present
    if attendance_data.hours_worked is not None:
        attendance.hours_worked = attendance_data.hours_worked
    if attendance_data.date is not None:
        attendance.date = attendance_data.date
    if attendance_data.site_name is not None:
        attendance.site_name = attendance_data.site_name

    await db.commit()
    await db.refresh(attendance)

    # Return the updated attendance, including the laborer's name
    return schemas.Attendance(
        id=attendance.id,
        laborer_id=attendance.laborer_id,
        laborer_name=attendance.laborer.name,  # Fetch laborer name from related model
        date=attendance.date,
        present=attendance.present,
        hours_worked=attendance.hours_worked,
        site_name=attendance.site_name
    )


## Material Invetory Codes

async def create_material(db: AsyncSession, material: schemas.MaterialCreate) -> schemas.Material:
    # Check if the site_id exists
    site = await db.get(Site, material.site_id)
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    
    try:
        new_material = models.Material(**material.model_dump())
        db.add(new_material)
        await db.commit()
        await db.refresh(new_material)

        # Return the material including site_name
        return schemas.Material(
            id=new_material.id,
            name=new_material.name,
            quantity=new_material.quantity,
            unit=new_material.unit,
            site_id=new_material.site_id,
            arrival_date=new_material.arrival_date,
            transport_type=new_material.transport_type,
            site_name=site.name  # Include the site name here
        )
    except SQLAlchemyError as e:
        print(f"Database error occurred while creating material: {e}")
        raise HTTPException(status_code=500, detail="Failed to create material")

async def get_material(db: AsyncSession, material_id: int) -> Optional[schemas.Material]:
    try:
        query = select(Material).options(joinedload(Material.site)).where(Material.id == material_id)
        result = await db.execute(query)
        material = result.scalar_one_or_none()
        if material:
            return schemas.Material(
                id=material.id,
                name=material.name,
                quantity=material.quantity,
                unit=material.unit,
                site_id=material.site_id,
                arrival_date=material.arrival_date,
                transport_type=material.transport_type,
                site_name=material.site.name if material.site else None  # Ensure site name is included
            )
        return None
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while fetching material by id {material_id}: {e}")
        raise HTTPException(status_code=500, detail="Database error occurred")


async def get_materials(db: AsyncSession, skip: int = 0, limit: int = 10) -> List[Material]:
    try:
        query = select(Material).options(joinedload(Material.site)).offset(skip).limit(limit)
        result = await db.execute(query)
        materials = result.scalars().all()
        
        return [{
            "id": mat.id,
            "name": mat.name,
            "quantity": mat.quantity,
            "unit": mat.unit,
            "site_id": mat.site_id,
            "site_name": mat.site.name if mat.site else None,
            "arrival_date": mat.arrival_date,
            "transport_type": mat.transport_type
        } for mat in materials]
    except Exception as e:
        logger.error("Error fetching materials", exc_info=e)
        raise HTTPException(status_code=500, detail="Database error occurred")


async def update_material(db: AsyncSession, material_id: int, material: schemas.MaterialUpdate) -> schemas.Material:
    # Update directly using the material ID
    query = (
        update(Material)
        .where(Material.id == material_id)
        .values(
            name=material.name,
            quantity=material.quantity,
            unit=material.unit,
            site_id=material.site_id,
            arrival_date=material.arrival_date,
            transport_type=material.transport_type
        )
    )

    try:
        result = await db.execute(query)
        if result.rowcount == 0:
            raise HTTPException(status_code=404, detail="Material not found or no changes made.")
        await db.commit()  # Commit the changes
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while updating material {material_id}: {e}")
        await db.rollback()  # Roll back in case of error
        raise HTTPException(status_code=500, detail="Database error occurred")

    # Return updated material details, assuming you want to retrieve them afterward
    updated_material = await db.get(Material, material_id)
    return schemas.Material(
        id=updated_material.id,
        name=updated_material.name,
        quantity=updated_material.quantity,
        unit=updated_material.unit,
        site_id=updated_material.site_id,
        arrival_date=updated_material.arrival_date,
        transport_type=updated_material.transport_type,
        site_name='Unknown'
    )

async def delete_material(db: AsyncSession, material_id: int) -> Optional[schemas.Material]:
    try:
        # Fetch the material to ensure it exists
        material = await db.get(Material, material_id)
        
        if not material:
            return None  # Return None if no material is found with that ID

        await db.delete(material)  # Delete the material
        await db.commit()  # Commit the changes
        return schemas.Material(
            id=material.id,
            name=material.name,
            quantity=material.quantity,
            unit=material.unit,
            site_id=material.site_id,
            arrival_date=material.arrival_date,
            transport_type=material.transport_type,
            site_name='Unknown'
        )
    except SQLAlchemyError as e:
        logger.error(f"Database error occurred while deleting material {material_id}: {e}")
        await db.rollback()  # Roll back in case of error
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logger.error(f"Unexpected error occurred while deleting material {material_id}: {e}")
        await db.rollback()  # Roll back for any other exceptions
        raise HTTPException(status_code=500, detail="An unexpected error occurred")
    
## SITES

async def create_site(db: AsyncSession, site: schemas.SiteCreate) -> schemas.Site:
    try:
        # Create a new site using model_dump to convert to a dict
        new_site = models.Site(**site.model_dump())
        db.add(new_site)
        await db.commit()
        await db.refresh(new_site)  # Refresh to get the auto-generated id
        return new_site
    except SQLAlchemyError as e:
        # Log the error (you can replace this with your logging mechanism)
        print(f"Database error occurred while creating site: {e}")
        raise HTTPException(status_code=500, detail="Failed to create site")  # Raise a 500 error
    except Exception as e:
        # Handle unexpected exceptions
        print(f"Unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

async def get_sites(db: AsyncSession, skip: int = 0, limit: int = 10):
    try:
        # Use `select` to get the sites from the database
        result = await db.execute(select(Site).offset(skip).limit(limit))
        return result.scalars().all()  # Return the list of sites
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")

async def get_site(db: AsyncSession, site_id: int) -> Site:
    site = await db.get(Site, site_id)
    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    return site

async def update_site(db: AsyncSession, site_id: int, site_data: schemas.SiteCreate) -> Site:
    site = await db.get(Site, site_id)
    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")

    for key, value in site_data.model_dump().items():
        setattr(site, key, value)
    db.add(site)
    await db.commit()
    await db.refresh(site)
    return site

async def delete_site(db: AsyncSession, site_id: int) -> bool:
    site = await db.get(Site, site_id)
    if site is None:
        raise HTTPException(status_code=404, detail="Site not found")
    await db.delete(site)
    await db.commit()
    return True