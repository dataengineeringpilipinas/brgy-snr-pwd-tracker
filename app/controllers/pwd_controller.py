"""PWD controller."""
from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException

from app.models.pwd import PWD, PWDCreate, PWDUpdate, PWDResponse


async def create_pwd(db: AsyncSession, pwd: PWDCreate) -> PWDResponse:
    """Create a new PWD."""
    db_pwd = PWD(**pwd.model_dump())
    db.add(db_pwd)
    await db.commit()
    await db.refresh(db_pwd)
    return PWDResponse.model_validate(db_pwd)


async def get_pwd(db: AsyncSession, pwd_id: int) -> Optional[PWDResponse]:
    """Get a specific PWD by ID."""
    result = await db.execute(select(PWD).where(PWD.id == pwd_id))
    pwd = result.scalar_one_or_none()
    return PWDResponse.model_validate(pwd) if pwd else None


async def get_pwds(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    barangay: Optional[str] = None,
    is_active: Optional[bool] = None
) -> List[PWDResponse]:
    """Get all PWDs with optional filtering."""
    query = select(PWD)
    
    if barangay:
        query = query.where(PWD.barangay == barangay)
    if is_active is not None:
        query = query.where(PWD.is_active == is_active)
    
    query = query.offset(skip).limit(limit).order_by(PWD.last_name, PWD.first_name)
    result = await db.execute(query)
    pwds = result.scalars().all()
    return [PWDResponse.model_validate(pwd) for pwd in pwds]


async def update_pwd(
    db: AsyncSession,
    pwd_id: int,
    pwd_update: PWDUpdate
) -> PWDResponse:
    """Update a PWD."""
    result = await db.execute(select(PWD).where(PWD.id == pwd_id))
    pwd = result.scalar_one_or_none()
    
    if not pwd:
        raise HTTPException(status_code=404, detail="PWD not found")
    
    update_data = pwd_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = date.today()
    
    for field, value in update_data.items():
        setattr(pwd, field, value)
    
    await db.commit()
    await db.refresh(pwd)
    return PWDResponse.model_validate(pwd)


async def delete_pwd(db: AsyncSession, pwd_id: int) -> bool:
    """Delete a PWD."""
    result = await db.execute(select(PWD).where(PWD.id == pwd_id))
    pwd = result.scalar_one_or_none()
    
    if not pwd:
        raise HTTPException(status_code=404, detail="PWD not found")
    
    await db.delete(pwd)
    await db.commit()
    return True

