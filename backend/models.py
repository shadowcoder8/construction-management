import enum
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float,Enum
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


# Material Inventory Codes

class UnitType(enum.Enum):
    kg = "kg"
    liter = "liter"
    ton = "ton"
    piece = "piece"
    cubic_meter = "cubic_meter"
    bag = "bag"
    gallon = "gallon"
    pound = "pound"
    ounce = "ounce"
    metric_ton = "metric_ton"
    square_meter = "square_meter"
    cubic_foot = "cubic_foot"
    liter_per_kilometer = "liter/km"
    milliliter = "ml"
    centiliter = "cl"
    hectare = "ha"
    acre = "acre"
    barrel = "barrel"
    dozen = "dozen"
    crate = "crate"
    pallet = "pallet"
    roll = "roll"
    nos = "nos"
    piece_per_box = "pieces/box"

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Float, nullable=False)
    unit = Column(Enum(UnitType), nullable=False)  # Use Enum for unit
    site_id = Column(Integer, ForeignKey("sites.id"))
    arrival_date = Column(Date, nullable=False)  # Date of arrival
    transport_type = Column(String, nullable=True)  # Optional transport type

    site = relationship("Site", back_populates="materials")

class Site(Base):
    __tablename__ = "sites"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    location = Column(String, nullable=True)

    materials = relationship("Material", back_populates="site")
