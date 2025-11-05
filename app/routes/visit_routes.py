"""Visit routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.controllers import visit_controller
from app.models.visit import VisitCreate, VisitUpdate, VisitResponse

router = APIRouter(prefix="/api/visits", tags=["visits"])


@router.post("", response_model=VisitResponse, status_code=201)
async def create_visit(
    visit: VisitCreate,
    db: AsyncSession = Depends(get_db)
) -> VisitResponse:
    """Create a new visit."""
    return await visit_controller.create_visit(db, visit)


@router.get("", response_model=List[VisitResponse])
async def get_visits(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    beneficiary_type: Optional[str] = Query(None),
    beneficiary_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db)
) -> List[VisitResponse]:
    """Get all visits."""
    return await visit_controller.get_visits(
        db, skip, limit, beneficiary_type, beneficiary_id, status
    )


@router.get("/{visit_id}", response_model=VisitResponse)
async def get_visit(
    visit_id: int,
    db: AsyncSession = Depends(get_db)
) -> VisitResponse:
    """Get a specific visit."""
    visit = await visit_controller.get_visit(db, visit_id)
    if not visit:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Visit not found")
    return visit


@router.put("/{visit_id}", response_model=VisitResponse)
async def update_visit(
    visit_id: int,
    visit_update: VisitUpdate,
    db: AsyncSession = Depends(get_db)
) -> VisitResponse:
    """Update a visit."""
    return await visit_controller.update_visit(db, visit_id, visit_update)


@router.delete("/{visit_id}", status_code=204)
async def delete_visit(
    visit_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a visit."""
    await visit_controller.delete_visit(db, visit_id)
    return None

