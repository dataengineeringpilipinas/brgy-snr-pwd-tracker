"""Web routes for HTML templates."""
from typing import List
from fastapi import APIRouter, Depends, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.controllers import (
    senior_controller,
    pwd_controller,
    benefit_controller,
    visit_controller,
    assistance_drive_controller
)

templates = Jinja2Templates(directory="app/templates")
router = APIRouter()


@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request, db: AsyncSession = Depends(get_db)):
    """Dashboard page."""
    # Get counts for dashboard
    seniors = await senior_controller.get_seniors(db, skip=0, limit=1000)
    pwds = await pwd_controller.get_pwds(db, skip=0, limit=1000)
    benefits = await benefit_controller.get_benefits(db, skip=0, limit=1000)
    visits = await visit_controller.get_visits(db, skip=0, limit=1000)
    drives = await assistance_drive_controller.get_assistance_drives(db, skip=0, limit=1000)
    
    active_seniors = len([s for s in seniors if s.is_active])
    active_pwds = len([p for p in pwds if p.is_active])
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "total_seniors": len(seniors),
        "active_seniors": active_seniors,
        "total_pwds": len(pwds),
        "active_pwds": active_pwds,
        "total_benefits": len(benefits),
        "pending_benefits": len([b for b in benefits if b.status == "pending"]),
        "total_visits": len(visits),
        "scheduled_visits": len([v for v in visits if v.status == "scheduled"]),
        "total_drives": len(drives),
        "ongoing_drives": len([d for d in drives if d.status == "ongoing"])
    })


@router.get("/seniors", response_class=HTMLResponse)
async def seniors_list(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    barangay: str = Query(None),
    is_active: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Senior citizens list page."""
    # Convert string to boolean if provided
    is_active_bool = None
    if is_active is not None:
        is_active_bool = is_active.lower() == "true"
    
    seniors = await senior_controller.get_seniors(db, skip, limit, barangay, is_active_bool)
    return templates.TemplateResponse("seniors.html", {
        "request": request,
        "seniors": seniors,
        "skip": skip,
        "limit": limit,
        "barangay": barangay,
        "is_active": is_active_bool
    })


@router.get("/pwds", response_class=HTMLResponse)
async def pwds_list(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    barangay: str = Query(None),
    is_active: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """PWDs list page."""
    # Convert string to boolean if provided
    is_active_bool = None
    if is_active is not None:
        is_active_bool = is_active.lower() == "true"
    
    pwds = await pwd_controller.get_pwds(db, skip, limit, barangay, is_active_bool)
    return templates.TemplateResponse("pwds.html", {
        "request": request,
        "pwds": pwds,
        "skip": skip,
        "limit": limit,
        "barangay": barangay,
        "is_active": is_active_bool
    })


@router.get("/benefits", response_class=HTMLResponse)
async def benefits_list(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    status: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Benefits list page."""
    benefits = await benefit_controller.get_benefits(db, skip, limit, None, None, status)
    return templates.TemplateResponse("benefits.html", {
        "request": request,
        "benefits": benefits,
        "skip": skip,
        "limit": limit,
        "status": status
    })


@router.get("/visits", response_class=HTMLResponse)
async def visits_list(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    status: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Visits list page."""
    visits = await visit_controller.get_visits(db, skip, limit, None, None, status)
    return templates.TemplateResponse("visits.html", {
        "request": request,
        "visits": visits,
        "skip": skip,
        "limit": limit,
        "status": status
    })


@router.get("/assistance-drives", response_class=HTMLResponse)
async def assistance_drives_list(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=1000),
    status: str = Query(None),
    db: AsyncSession = Depends(get_db)
):
    """Assistance drives list page."""
    drives = await assistance_drive_controller.get_assistance_drives(db, skip, limit, status, None)
    return templates.TemplateResponse("assistance_drives.html", {
        "request": request,
        "drives": drives,
        "skip": skip,
        "limit": limit,
        "status": status
    })

