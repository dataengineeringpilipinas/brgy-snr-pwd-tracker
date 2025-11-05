"""Benefit distribution model."""
from datetime import date
from typing import Optional
from sqlmodel import SQLModel, Field


class BenefitBase(SQLModel):
    """Base model for Benefit."""
    beneficiary_type: str = Field(..., max_length=20)  # "senior" or "pwd"
    beneficiary_id: int
    benefit_type: str = Field(..., max_length=100)
    amount: Optional[float] = Field(None)
    description: Optional[str] = Field(None, max_length=500)
    distribution_date: date
    distributed_by: Optional[str] = Field(None, max_length=100)
    status: str = Field(default="pending", max_length=20)  # pending, distributed, cancelled


class Benefit(BenefitBase, table=True):
    """Benefit database model."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[date] = Field(default_factory=date.today)
    updated_at: Optional[date] = Field(default_factory=date.today)


class BenefitCreate(BenefitBase):
    """Schema for creating a Benefit."""
    pass


class BenefitUpdate(SQLModel):
    """Schema for updating a Benefit."""
    benefit_type: Optional[str] = None
    amount: Optional[float] = None
    description: Optional[str] = None
    distribution_date: Optional[date] = None
    distributed_by: Optional[str] = None
    status: Optional[str] = None


class BenefitResponse(BenefitBase):
    """Schema for Benefit response."""
    id: int
    created_at: date
    updated_at: date

