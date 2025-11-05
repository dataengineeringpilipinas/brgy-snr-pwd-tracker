"""Visit controller."""
from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException

from app.models.visit import Visit, VisitCreate, VisitUpdate, VisitResponse


async def create_visit(db: AsyncSession, visit: VisitCreate) -> VisitResponse:
    """Create a new visit."""
    db_visit = Visit(**visit.model_dump())
    db.add(db_visit)
    await db.commit()
    await db.refresh(db_visit)
    return VisitResponse.model_validate(db_visit)


async def get_visit(db: AsyncSession, visit_id: int) -> Optional[VisitResponse]:
    """Get a specific visit by ID."""
    result = await db.execute(select(Visit).where(Visit.id == visit_id))
    visit = result.scalar_one_or_none()
    return VisitResponse.model_validate(visit) if visit else None


async def get_visits(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    beneficiary_type: Optional[str] = None,
    beneficiary_id: Optional[int] = None,
    status: Optional[str] = None
) -> List[VisitResponse]:
    """Get all visits with optional filtering."""
    query = select(Visit)
    
    if beneficiary_type:
        query = query.where(Visit.beneficiary_type == beneficiary_type)
    if beneficiary_id:
        query = query.where(Visit.beneficiary_id == beneficiary_id)
    if status:
        query = query.where(Visit.status == status)
    
    query = query.offset(skip).limit(limit).order_by(Visit.visit_date.desc())
    result = await db.execute(query)
    visits = result.scalars().all()
    return [VisitResponse.model_validate(visit) for visit in visits]


async def update_visit(
    db: AsyncSession,
    visit_id: int,
    visit_update: VisitUpdate
) -> VisitResponse:
    """Update a visit."""
    result = await db.execute(select(Visit).where(Visit.id == visit_id))
    visit = result.scalar_one_or_none()
    
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    update_data = visit_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = datetime.now()
    
    for field, value in update_data.items():
        setattr(visit, field, value)
    
    await db.commit()
    await db.refresh(visit)
    return VisitResponse.model_validate(visit)


async def delete_visit(db: AsyncSession, visit_id: int) -> bool:
    """Delete a visit."""
    result = await db.execute(select(Visit).where(Visit.id == visit_id))
    visit = result.scalar_one_or_none()
    
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    
    await db.delete(visit)
    await db.commit()
    return True

