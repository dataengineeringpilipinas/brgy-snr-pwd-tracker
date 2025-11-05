"""Assistance Drive controller."""
from typing import List, Optional
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from fastapi import HTTPException

from app.models.assistance_drive import (
    AssistanceDrive,
    AssistanceDriveCreate,
    AssistanceDriveUpdate,
    AssistanceDriveResponse
)


async def create_assistance_drive(
    db: AsyncSession,
    drive: AssistanceDriveCreate
) -> AssistanceDriveResponse:
    """Create a new assistance drive."""
    db_drive = AssistanceDrive(**drive.model_dump())
    db.add(db_drive)
    await db.commit()
    await db.refresh(db_drive)
    return AssistanceDriveResponse.model_validate(db_drive)


async def get_assistance_drive(
    db: AsyncSession,
    drive_id: int
) -> Optional[AssistanceDriveResponse]:
    """Get a specific assistance drive by ID."""
    result = await db.execute(select(AssistanceDrive).where(AssistanceDrive.id == drive_id))
    drive = result.scalar_one_or_none()
    return AssistanceDriveResponse.model_validate(drive) if drive else None


async def get_assistance_drives(
    db: AsyncSession,
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    target_beneficiaries: Optional[str] = None
) -> List[AssistanceDriveResponse]:
    """Get all assistance drives with optional filtering."""
    query = select(AssistanceDrive)
    
    if status:
        query = query.where(AssistanceDrive.status == status)
    if target_beneficiaries:
        query = query.where(AssistanceDrive.target_beneficiaries == target_beneficiaries)
    
    query = query.offset(skip).limit(limit).order_by(AssistanceDrive.start_date.desc())
    result = await db.execute(query)
    drives = result.scalars().all()
    return [AssistanceDriveResponse.model_validate(drive) for drive in drives]


async def update_assistance_drive(
    db: AsyncSession,
    drive_id: int,
    drive_update: AssistanceDriveUpdate
) -> AssistanceDriveResponse:
    """Update an assistance drive."""
    result = await db.execute(select(AssistanceDrive).where(AssistanceDrive.id == drive_id))
    drive = result.scalar_one_or_none()
    
    if not drive:
        raise HTTPException(status_code=404, detail="Assistance drive not found")
    
    update_data = drive_update.model_dump(exclude_unset=True)
    update_data["updated_at"] = date.today()
    
    for field, value in update_data.items():
        setattr(drive, field, value)
    
    await db.commit()
    await db.refresh(drive)
    return AssistanceDriveResponse.model_validate(drive)


async def delete_assistance_drive(db: AsyncSession, drive_id: int) -> bool:
    """Delete an assistance drive."""
    result = await db.execute(select(AssistanceDrive).where(AssistanceDrive.id == drive_id))
    drive = result.scalar_one_or_none()
    
    if not drive:
        raise HTTPException(status_code=404, detail="Assistance drive not found")
    
    await db.delete(drive)
    await db.commit()
    return True

