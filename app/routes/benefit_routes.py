"""Benefit routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.controllers import benefit_controller
from app.models.benefit import BenefitCreate, BenefitUpdate, BenefitResponse

router = APIRouter(prefix="/api/benefits", tags=["benefits"])


@router.post("", response_model=BenefitResponse, status_code=201)
async def create_benefit(
    benefit: BenefitCreate,
    db: AsyncSession = Depends(get_db)
) -> BenefitResponse:
    """Create a new benefit."""
    return await benefit_controller.create_benefit(db, benefit)


@router.get("", response_model=List[BenefitResponse])
async def get_benefits(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    beneficiary_type: Optional[str] = Query(None),
    beneficiary_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
) -> List[BenefitResponse]:
    """Get all benefits."""
    return await benefit_controller.get_benefits(
        db, skip, limit, beneficiary_type, beneficiary_id, status
    )


@router.get("/{benefit_id}", response_model=BenefitResponse)
async def get_benefit(
    benefit_id: int,
    db: AsyncSession = Depends(get_db)
) -> BenefitResponse:
    """Get a specific benefit."""
    benefit = await benefit_controller.get_benefit(db, benefit_id)
    if not benefit:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Benefit not found")
    return benefit


@router.put("/{benefit_id}", response_model=BenefitResponse)
async def update_benefit(
    benefit_id: int,
    benefit_update: BenefitUpdate,
    db: AsyncSession = Depends(get_db)
) -> BenefitResponse:
    """Update a benefit."""
    return await benefit_controller.update_benefit(db, benefit_id, benefit_update)


@router.delete("/{benefit_id}", status_code=204)
async def delete_benefit(
    benefit_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a benefit."""
    await benefit_controller.delete_benefit(db, benefit_id)
    return None

