from pydantic import BaseModel
from datetime import date
from backend.models import UnitType
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

## Material Inventory Codes

# Material Schema
class MaterialBase(BaseModel):
    name: str
    quantity: float
    unit: UnitType
    site_id: int
    arrival_date: date
    transport_type: Optional[str]  # Optional field for transport type

class MaterialCreate(MaterialBase):
    pass

class MaterialUpdate(MaterialBase):
    pass

class Material(MaterialBase):
    id: int
    site_name: Optional[str]  # To include the site name in the response

    class Config:
        from_attributes = True

# Site Schema
class SiteBase(BaseModel):
    name: str
    location: str

class SiteCreate(SiteBase):
   pass

class SiteUpdate(SiteBase):
   pass

class Site(SiteBase):
    id: int

    class Config:
        from_attributes = True


# Payment Schemas 
class PaymentBase(BaseModel):
    amount: float
    date: date
    labor_id: int
    site_id: int
    material_name: Optional[str] = None  # To include the material name in the response
    description: Optional[str] = None  # Optional description for the payment

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(PaymentBase):
    pass

class Payment(PaymentBase):
    id: int
    labor_name: str  # To include the labor name in the response
    site_name: str   # To include the site name in the response
    class Config:
        from_attributes = True  # Allow ORM mode for easy data conversion
# Paginated Response
class PaginatedMaterialsResponse(BaseModel):
    results: List[Material]
    total: int
    next: Optional[int] = None
    prev: Optional[int] = None



