"""PWD routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.controllers import pwd_controller
from app.models.pwd import PWDCreate, PWDUpdate, PWDResponse

router = APIRouter(prefix="/api/pwds", tags=["pwds"])


@router.post("", response_model=PWDResponse, status_code=201)
async def create_pwd(
    pwd: PWDCreate,
    db: AsyncSession = Depends(get_db)
) -> PWDResponse:
    """Create a new PWD."""
    return await pwd_controller.create_pwd(db, pwd)


@router.get("", response_model=List[PWDResponse])
async def get_pwds(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    barangay: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None),
    db: AsyncSession = Depends(get_db)
) -> List[PWDResponse]:
    """Get all PWDs."""
    return await pwd_controller.get_pwds(db, skip, limit, barangay, is_active)


@router.get("/{pwd_id}", response_model=PWDResponse)
async def get_pwd(
    pwd_id: int,
    db: AsyncSession = Depends(get_db)
) -> PWDResponse:
    """Get a specific PWD."""
    pwd = await pwd_controller.get_pwd(db, pwd_id)
    if not pwd:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="PWD not found")
    return pwd


@router.put("/{pwd_id}", response_model=PWDResponse)
async def update_pwd(
    pwd_id: int,
    pwd_update: PWDUpdate,
    db: AsyncSession = Depends(get_db)
) -> PWDResponse:
    """Update a PWD."""
    return await pwd_controller.update_pwd(db, pwd_id, pwd_update)


@router.delete("/{pwd_id}", status_code=204)
async def delete_pwd(
    pwd_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Delete a PWD."""
    await pwd_controller.delete_pwd(db, pwd_id)
    return None

