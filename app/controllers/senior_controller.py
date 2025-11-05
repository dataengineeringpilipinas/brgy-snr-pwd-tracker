"""Senior Citizen controller."""
from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException

from app.models.senior import Senior, SeniorCreate, SeniorUpdate, SeniorResponse


async def create_senior(db: AsyncSession, senior: SeniorCreate) -> SeniorResponse:
    """Create a new senior citizen."""
    db_senior = Senior(**senior.model_dump())
    db.add(db_senior)
    await db.commit()
    await db.refresh(db_senior)
    return SeniorResponse.model_validate(db_senior)


async def get_senior(db: AsyncSession, senior_id: int) -> Optional[SeniorResponse]:
    """Get a specific senior citizen by ID."""
    result = await db.execute(select(Senior).where(Senior.id == senior_id))
    senior = result.scalar_one_or_none()
    return SeniorResponse.model_validate(senior) if senior else None


async def get_seniors(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    barangay: Optional[str] = None,
    is_active: Optional[bool] = None
) -> List[SeniorResponse]:
    """Get all senior citizens with optional filtering."""
    query = select(Senior)
    
    if barangay:
        query = query.where(Senior.barangay == barangay)
    if is_active is not None:
        query = query.where(Senior.is_active == is_active)
    
    query = query.offset(skip).limit(limit).order_by(Senior.last_name, Senior.first_name)
    result = await db.execute(query)
    seniors = result.scalars().all()
    return [SeniorResponse.model_validate(senior) for senior in seniors]


async def update_senior(
    db: AsyncSession,
    senior_id: int,
    senior_update: SeniorUpdate
) -> SeniorResponse:
    """Update a senior citizen."""
    result = await db.execute(select(Senior).where(Senior.id == senior_id))
    senior = result.scalar_one_or_none()
    
    if not senior:
        raise HTTPException(status_code=404, detail="Senior citizen not found")
    
    update_data = senior_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = date.today()
    
    for field, value in update_data.items():
        setattr(senior, field, value)
    
    await db.commit()
    await db.refresh(senior)
    return SeniorResponse.model_validate(senior)


async def delete_senior(db: AsyncSession, senior_id: int) -> bool:
    """Delete a senior citizen."""
    result = await db.execute(select(Senior).where(Senior.id == senior_id))
    senior = result.scalar_one_or_none()
    
    if not senior:
        raise HTTPException(status_code=404, detail="Senior citizen not found")
    
    await db.delete(senior)
    await db.commit()
    return True

