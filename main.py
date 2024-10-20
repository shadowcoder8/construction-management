from fastapi import FastAPI, HTTPException, Depends, Request, Response,Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession
from backend import crud, models, schemas
from backend.database import engine, get_db
from sqlalchemy import select
import os
from sqlalchemy.exc import SQLAlchemyError
import logging
import uvicorn

logging.basicConfig(level=logging.INFO)

# Lifespan event for startup and shutdown
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        # Create the database tables
        await conn.run_sync(models.Base.metadata.create_all)
    yield
    # Clean up resources if needed on shutdown
    await engine.dispose()

app = FastAPI(lifespan=lifespan)

# Enable CORS (Cross-Origin Resource Sharing)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (HTML, CSS, JS) from the 'frontend' directory
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Simulated session storage
sessions = {}

# Serve the login page at the root URL
@app.get("/", response_class=HTMLResponse)
async def read_root():
    # Load and return the login.html file
    with open(os.path.join("frontend", "login.html")) as file:
        return file.read()

# Admin login route
@app.post("/admin/login/")
async def admin_login(login_request: models.LoginRequest, response: Response):
    from backend.auth import authenticate_admin
    try:
        authenticate_admin(login_request.username, login_request.password)
        # Create a session for the admin user
        session_id = login_request.username  # For simplicity, using username as session id
        sessions[session_id] = True  # Store session
        response.set_cookie("session_id", session_id)
        return {"message": "Login successful"}
    except Exception as e:
        logging.error(f"Login failed for {login_request.username}: {str(e)}")
        raise HTTPException(status_code=401, detail=str(e))  # Unauthorized

# Admin logout route
@app.post("/admin/logout/")
async def admin_logout(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id in sessions:
        del sessions[session_id]  # Remove session
    return {"message": "Logout successful"}

# Dependency to check if user is authenticated
async def get_current_user(request: Request):
    session_id = request.cookies.get("session_id")
    if session_id not in sessions:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return session_id

# Dashboard route
@app.get("/admin/dashboard/", response_class=HTMLResponse)
async def admin_dashboard(current_user: str = Depends(get_current_user)):
    # Load and return the dashboard.html file
    with open(os.path.join("frontend", "dashboard.html")) as file:
        return file.read()

@app.get("/labor-management/", response_class=HTMLResponse)
async def labor_management(current_user: str = Depends(get_current_user)):
    # Load and return the labor_management.html file
    with open(os.path.join("frontend", "labor-management.html")) as file:
        return file.read()

## Labour details

# Create Labour
@app.post("/labours/", response_model=schemas.Laborer)
async def create_labour(labour: schemas.LaborerCreate, db: AsyncSession = Depends(get_db)):
    logging.info(f"Received labour data: {labour}")  # Log incoming data
    try:
        return await crud.create_labour(db, labour)
    except SQLAlchemyError as e:
        logging.error(f"Database error while creating labour: {e}")  # Log the error for debugging
        raise HTTPException(status_code=500, detail="Database error occurred")
    except Exception as e:
        logging.error(f"Unexpected error while creating labour: {e}")  # Log the unexpected error
        raise HTTPException(status_code=500, detail="An unexpected error occurred")

# Get All Labours
@app.get("/labours/", response_model=list[schemas.Laborer])
async def read_labours(skip: int = 0, limit: int = 10, db: AsyncSession = Depends(get_db)):
    try:
        labours = await crud.get_labours(db=db, skip=skip, limit=limit)
        return labours
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")  # Generic error message

# Search Labours by Name
@app.get("/labours/search/", response_model=list[schemas.Laborer])
async def search_labours(name: str, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.search_labours(db, name)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")  # Generic error message

# Get a single Labour by ID
@app.get("/labours/{labour_id}", response_model=schemas.Laborer)
async def get_labour(labour_id: int, db: AsyncSession = Depends(get_db)):
    try:
        labour = await crud.get_labour(db, labour_id)
        if labour is None:
            raise HTTPException(status_code=404, detail="Labour not found")
        return labour
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")  # Generic error message

# Update Labour
@app.put("/labours/{labour_id}", response_model=schemas.LaborerUpdate)
async def update_labour(labour_id: int, updated_data: schemas.LaborerCreate, db: AsyncSession = Depends(get_db)):
    try:
        labour = await crud.update_labour(db, labour_id, updated_data)
        if labour is None:
            raise HTTPException(status_code=404, detail="Labour not found")
        return labour
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")  # Generic error message

# Delete Labour
@app.delete("/labours/{labour_id}")
async def delete_labour(labour_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await crud.delete_labour(db, labour_id)
        if not result:
            raise HTTPException(status_code=404, detail="Labour not found")
        return {"message": "Labour deleted successfully"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")  # Generic error message

# Record Attendance
@app.post("/labours/{labour_id}/attendance/", response_model=schemas.Attendance)
async def record_attendance(labour_id: int, attendance_data: schemas.AttendanceCreate, db: AsyncSession = Depends(get_db)):
    logging.info(f"Received labour attendance: {attendance_data}")
    try:
        # Call the CRUD function to create attendance
        new_attendance = await crud.create_attendance(db, labour_id, attendance_data)

        # Fetch the laborer name to include in the response
        laborer = await db.execute(select(models.Laborer).filter(models.Laborer.id == labour_id))
        laborer = laborer.scalar_one_or_none()

        if laborer is None:
            raise HTTPException(status_code=404, detail="Laborer not found")

        # Return the newly created attendance with laborer_name
        return schemas.Attendance(
            id=new_attendance.id,
            laborer_id=new_attendance.laborer_id,
            laborer_name=laborer.name,
            date=new_attendance.date,
            present=new_attendance.present,
            hours_worked=new_attendance.hours_worked,
            site_name=new_attendance.site_name
        )
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")


# Get Attendance History
@app.get("/labours/{labour_id}/attendance/", response_model=list[schemas.Attendance])
async def get_attendance_history(labour_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await crud.get_attendance_history(db, labour_id)
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")  # Generic error message

# Get All Attendance Records with Pagination
@app.get("/attendance/", response_model=schemas.AttendanceResponse)  # Adjust to your schema
async def get_all_attendance(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),  # Starting point (offset)
    limit: int = Query(10, gt=0, le=100)  # Number of records to return
):
    try:
        attendance_records = await crud.get_all_attendance(db, skip=skip, limit=limit)
        
        total_count = await crud.count_all_attendance(db)  # Get total count for pagination
        return {
            "results": attendance_records,
            "next": skip + limit if (skip + limit) < total_count else None,  # Calculate next page
            "prev": skip - limit if skip > 0 else None,  # Calculate previous page
            "total": total_count  # Total count for reference
        }
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")

# Get Attendance by ID
@app.get("/attendance/{attendance_id}", response_model=schemas.Attendance)
async def get_attendance(attendance_id: int, db: AsyncSession = Depends(get_db)):
    try:
        attendance = await crud.get_attendance(db, attendance_id)
        if attendance is None:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return attendance
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")  # Generic error message


# Update Attendance Record
@app.put("/attendance/{attendance_id}", response_model=schemas.Attendance)
async def update_attendance(attendance_id: int, attendance_data: schemas.AttendanceUpdate, db: AsyncSession = Depends(get_db)):
    try:
        updated_attendance = await crud.update_attendance(db, attendance_id, attendance_data)

        if updated_attendance is None:
            raise HTTPException(status_code=404, detail="Attendance record not found")

        return updated_attendance  # Return the updated attendance record
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")


# Delete Attendance Record
@app.delete("/attendance/{attendance_id}")
async def delete_attendance(attendance_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await crud.delete_attendance(db, attendance_id)
        if not result:
            raise HTTPException(status_code=404, detail="Attendance record not found")
        return {"message": "Attendance record deleted successfully"}
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error occurred")  # Generic error message

if __name == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
