from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from sqlalchemy.orm import relationship
from backend.database import Base
from pydantic import BaseModel

class Laborer(Base):
    __tablename__ = 'laborers'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    gender = Column(String)
    daily_wage = Column(Float)
    date_of_joining = Column(Date)

    attendance_records = relationship("Attendance", back_populates="laborer",cascade="all, delete-orphan")

class Attendance(Base):
    __tablename__ = 'attendance'

    id = Column(Integer, primary_key=True, index=True)
    laborer_id = Column(Integer, ForeignKey('laborers.id'))
    date = Column(Date)
    present = Column(String) 
    hours_worked = Column(Float)
    site_name = Column(String)

    laborer = relationship("Laborer", back_populates="attendance_records")

# Pydantic model for login
class LoginRequest(BaseModel):
    username: str
    password: str

# # Presence recording route (for laborers)
# class PresenceRequest(BaseModel):
#     laborer_id: int
#     hours_worked: float
#     present: bool

