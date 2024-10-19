from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,func  
from backend import models, schemas
from sqlalchemy.orm import selectinload,joinedload
from backend.models import Attendance


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
