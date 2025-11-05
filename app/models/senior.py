"""Senior Citizen model."""
from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field


class SeniorBase(SQLModel):
    """Base model for Senior Citizen."""
    first_name: str = Field(..., max_length=100)
    last_name: str = Field(..., max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    birth_date: date
    gender: str = Field(..., max_length=20)
    address: str = Field(..., max_length=255)
    contact_number: Optional[str] = Field(None, max_length=20)
    osca_id: Optional[str] = Field(None, max_length=50, unique=True)
    barangay: str = Field(..., max_length=100)
    is_active: bool = Field(default=True)
    notes: Optional[str] = Field(None, max_length=1000)


class Senior(SeniorBase, table=True):
    """Senior Citizen database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[date] = Field(default_factory=date.today)
    updated_at: Optional[date] = Field(default_factory=date.today)


class SeniorCreate(SeniorBase):
    """Schema for creating a Senior Citizen."""
    pass


class SeniorUpdate(SQLModel):
    """Schema for updating a Senior Citizen."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    osca_id: Optional[str] = None
    barangay: Optional[str] = None
    is_active: Optional[bool] = None
    notes: Optional[str] = None


class SeniorResponse(SeniorBase):
    """Schema for Senior Citizen response."""
    id: int
    created_at: date
    updated_at: date

