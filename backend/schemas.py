from pydantic import BaseModel
from datetime import date
from typing import List, Optional

class LaborerBase(BaseModel):
    name: str
    age: int
    gender: str
    daily_wage: float
    date_of_joining: date

class LaborerCreate(LaborerBase):
    pass

class LaborerUpdate(LaborerBase):
    pass

class Laborer(LaborerBase):
    id: int

    class Config:
        from_attributes = True

class AttendanceBase(BaseModel):
    laborer_id: int
    laborer_name: str
    date: date
    present: str
    hours_worked: float
    site_name: str

# Pydantic model for updating attendance
class AttendanceUpdate(BaseModel):
    present: Optional[str]
    hours_worked: Optional[float]
    date: Optional[date]
    site_name: Optional[str]

    class Config:
        from_attributes = True

class AttendanceCreate(BaseModel):
    laborer_id: int
    date: date  # Ensure this is the correct type for your date (could also be datetime)
    present: str  # or bool, depending on your schema definition
    hours_worked: float  # Ensure this matches the expected4
    site_name: str


class Attendance(AttendanceBase):
    id: int

    class Config:
        from_attributes = True

class AttendanceResponse(BaseModel):
    results: List[Attendance]  # This can be an empty list
    next: Optional[int] = None
    prev: Optional[int] = None
    total: int