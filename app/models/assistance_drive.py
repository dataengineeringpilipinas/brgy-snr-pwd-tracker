"""Assistance Drive model."""
from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field


class AssistanceDriveBase(SQLModel):
    """Base model for Assistance Drive."""
    drive_name: str = Field(..., max_length=200)
    drive_type: str = Field(..., max_length=50)  # medical, food, financial, etc.
    target_beneficiaries: str = Field(..., max_length=20)  # "senior", "pwd", or "both"
    start_date: date
    end_date: Optional[date] = None
    location: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=1000)
    organizer: Optional[str] = Field(None, max_length=100)
    status: str = Field(default="planned", max_length=20)  # planned, ongoing, completed, cancelled
    participants_count: Optional[int] = Field(default=0)


class AssistanceDrive(AssistanceDriveBase, table=True):
    """Assistance Drive database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[date] = Field(default_factory=date.today)
    updated_at: Optional[date] = Field(default_factory=date.today)


class AssistanceDriveCreate(AssistanceDriveBase):
    """Schema for creating an Assistance Drive."""
    pass


class AssistanceDriveUpdate(SQLModel):
    """Schema for updating an Assistance Drive."""
    drive_name: Optional[str] = None
    drive_type: Optional[str] = None
    target_beneficiaries: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    location: Optional[str] = None
    description: Optional[str] = None
    organizer: Optional[str] = None
    status: Optional[str] = None
    participants_count: Optional[int] = None


class AssistanceDriveResponse(AssistanceDriveBase):
    """Schema for Assistance Drive response."""
    id: int
    created_at: date
    updated_at: date

