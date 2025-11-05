"""Visit scheduling model."""
from datetime import date, datetime
from typing import Optional
from sqlmodel import SQLModel, Field


class VisitBase(SQLModel):
    """Base model for Visit."""
    beneficiary_type: str = Field(..., max_length=20)  # "senior" or "pwd"
    beneficiary_id: int
    visit_date: date
    visit_time: Optional[str] = Field(None, max_length=20)
    visit_type: str = Field(..., max_length=50)  # checkup, assessment, assistance, etc.
    purpose: Optional[str] = Field(None, max_length=500)
    visited_by: Optional[str] = Field(None, max_length=100)
    status: str = Field(default="scheduled", max_length=20)  # scheduled, completed, cancelled, rescheduled
    notes: Optional[str] = Field(None, max_length=1000)


class Visit(VisitBase, table=True):
    """Visit database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[datetime] = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = Field(default_factory=datetime.now)


class VisitCreate(VisitBase):
    """Schema for creating a Visit."""
    pass


class VisitUpdate(SQLModel):
    """Schema for updating a Visit."""
    visit_date: Optional[date] = None
    visit_time: Optional[str] = None
    visit_type: Optional[str] = None
    purpose: Optional[str] = None
    visited_by: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class VisitResponse(VisitBase):
    """Schema for Visit response."""
    id: int
    created_at: datetime
    updated_at: datetime

