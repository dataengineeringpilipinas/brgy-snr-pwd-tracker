"""Senior Citizen routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.controllers import senior_controller
from app.models.senior import SeniorCreate, SeniorUpdate, SeniorResponse

router = APIRouter(prefix="/api/seniors", tags=["seniors"])


@router.post("", response_model=SeniorResponse, status_code=201)
async def create_senior(
    senior: SeniorCreate,
    db: AsyncSession = Depends(get_db)
) -> SeniorResponse:
    """Create a new senior citizen."""
    return await senior_controller.create_senior(db, senior)


@router.get("", response_model=List[SeniorResponse])
async def get_seniors(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    barangay: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db)
) -> List[SeniorResponse]:
    """Get all senior citizens."""
    return await senior_controller.get_seniors(db, skip, limit, barangay, is_active)


@router.get("/{senior_id}", response_model=SeniorResponse)
async def get_senior(
    senior_id: int,
    db: AsyncSession = Depends(get_db)
) -> SeniorResponse:
    """Get a specific senior citizen."""
    senior = await senior_controller.get_senior(db, senior_id)
    if not senior:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Senior citizen not found")
    return senior


@router.put("/{senior_id}", response_model=SeniorResponse)
async def update_senior(
    senior_id: int,
    senior_update: SeniorUpdate,
    db: AsyncSession = Depends(get_db)
) -> SeniorResponse:
    """Update a senior citizen."""
    return await senior_controller.update_senior(db, senior_id, senior_update)


@router.delete("/{senior_id}", status_code=204)
async def delete_senior(
    senior_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a senior citizen."""
    await senior_controller.delete_senior(db, senior_id)
    return None

