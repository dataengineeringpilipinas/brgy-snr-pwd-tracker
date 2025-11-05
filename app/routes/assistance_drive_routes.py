"""Assistance Drive routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.controllers import assistance_drive_controller
from app.models.assistance_drive import (
    AssistanceDriveCreate,
    AssistanceDriveUpdate,
    AssistanceDriveResponse
)

router = APIRouter(prefix="/api/assistance-drives", tags=["assistance-drives"])


@router.post("", response_model=AssistanceDriveResponse, status_code=201)
async def create_assistance_drive(
    drive: AssistanceDriveCreate,
    db: AsyncSession = Depends(get_db)
) -> AssistanceDriveResponse:
    """Create a new assistance drive."""
    return await assistance_drive_controller.create_assistance_drive(db, drive)


@router.get("", response_model=List[AssistanceDriveResponse])
async def get_assistance_drives(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    status: Optional[str] = Query(None),
    target_beneficiaries: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
) -> List[AssistanceDriveResponse]:
    """Get all assistance drives."""
    return await assistance_drive_controller.get_assistance_drives(
        db, skip, limit, status, target_beneficiaries
    )


@router.get("/{drive_id}", response_model=AssistanceDriveResponse)
async def get_assistance_drive(
    drive_id: int,
    db: AsyncSession = Depends(get_db)
) -> AssistanceDriveResponse:
    """Get a specific assistance drive."""
    drive = await assistance_drive_controller.get_assistance_drive(db, drive_id)
    if not drive:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Assistance drive not found")
    return drive


@router.put("/{drive_id}", response_model=AssistanceDriveResponse)
async def update_assistance_drive(
    drive_id: int,
    drive_update: AssistanceDriveUpdate,
    db: AsyncSession = Depends(get_db)
) -> AssistanceDriveResponse:
    """Update an assistance drive."""
    return await assistance_drive_controller.update_assistance_drive(db, drive_id, drive_update)


@router.delete("/{drive_id}", status_code=204)
async def delete_assistance_drive(
    drive_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete an assistance drive."""
    await assistance_drive_controller.delete_assistance_drive(db, drive_id)
    return None

