"""Benefit controller."""
from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException

from app.models.benefit import Benefit, BenefitCreate, BenefitUpdate, BenefitResponse


async def create_benefit(db: AsyncSession, benefit: BenefitCreate) -> BenefitResponse:
    """Create a new benefit."""
    db_benefit = Benefit(**benefit.model_dump())
    db.add(db_benefit)
    await db.commit()
    await db.refresh(db_benefit)
    return BenefitResponse.model_validate(db_benefit)


async def get_benefit(db: AsyncSession, benefit_id: int) -> Optional[BenefitResponse]:
    """Get a specific benefit by ID."""
    result = await db.execute(select(Benefit).where(Benefit.id == benefit_id))
    benefit = result.scalar_one_or_none()
    return BenefitResponse.model_validate(benefit) if benefit else None


async def get_benefits(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    beneficiary_type: Optional[str] = None,
    beneficiary_id: Optional[int] = None,
    status: Optional[str] = None
) -> List[BenefitResponse]:
    """Get all benefits with optional filtering."""
    query = select(Benefit)
    
    if beneficiary_type:
        query = query.where(Benefit.beneficiary_type == beneficiary_type)
    if beneficiary_id:
        query = query.where(Benefit.beneficiary_id == beneficiary_id)
    if status:
        query = query.where(Benefit.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Benefit.distribution_date.desc())
    result = await db.execute(query)
    benefits = result.scalars().all()
    return [BenefitResponse.model_validate(benefit) for benefit in benefits]


async def update_benefit(
    db: AsyncSession,
    benefit_id: int,
    benefit_update: BenefitUpdate
) -> BenefitResponse:
    """Update a benefit."""
    result = await db.execute(select(Benefit).where(Benefit.id == benefit_id))
    benefit = result.scalar_one_or_none()
    
    if not benefit:
        raise HTTPException(status_code=404, detail="Benefit not found")
    
    update_data = benefit_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = date.today()
    
    for field, value in update_data.items():
        setattr(benefit, field, value)
    
    await db.commit()
    await db.refresh(benefit)
    return BenefitResponse.model_validate(benefit)


async def delete_benefit(db: AsyncSession, benefit_id: int) -> bool:
    """Delete a benefit."""
    result = await db.execute(select(Benefit).where(Benefit.id == benefit_id))
    benefit = result.scalar_one_or_none()
    
    if not benefit:
        raise HTTPException(status_code=404, detail="Benefit not found")
    
    await db.delete(benefit)
    await db.commit()
    return True

