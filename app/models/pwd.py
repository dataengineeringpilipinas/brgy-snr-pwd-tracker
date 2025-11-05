"""Person with Disability model."""
from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field


class PWDBase(SQLModel):
    """Base model for Person with Disability."""
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    birth_date: date
    gender: str = Field(..., max_length=20)
    address: str = Field(..., max_length=255)
    contact_number: Optional[str] = Field(None, max_length=20)
    pwd_id: Optional[str] = Field(None, max_length=50, unique=True)
    disability_type: str = Field(..., max_length=100)
    barangay: str = Field(..., max_length=100)
    is_active: bool = Field(default=True)
    notes: Optional[str] = Field(None, max_length=1000)


class PWD(PWDBase, table=True):
    """Person with Disability database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[date] = Field(default_factory=date.today)
    updated_at: Optional[date] = Field(default_factory=date.today)


class PWDCreate(PWDBase):
    """Schema for creating a Person with Disability."""
    pass


class PWDUpdate(SQLModel):
    """Schema for updating a Person with Disability."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    pwd_id: Optional[str] = None
    disability_type: Optional[str] = None
    barangay: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class PWDResponse(PWDBase):
    """Schema for PWD response."""
    id: int
    created_at: date
    updated_at: date

