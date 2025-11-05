"""Main FastAPI application."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database import init_db
from app.routes import (
    senior_routes,
    pwd_routes,
    benefit_routes,
    visit_routes,
    assistance_drive_routes,
    web_routes
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup
    await init_db()
    yield
    # Shutdown


app = FastAPI(
    title="Barangay Senior & PWD Support Tracker",
    description="App/Database for monitoring senior citizens and PWDs — for distributing benefits, scheduling visits, or organizing assistance drives.",
    version="1.0.0",
    lifespan=lifespan
)

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Include routers
app.include_router(web_routes.router)
app.include_router(senior_routes.router)
app.include_router(pwd_routes.router)
app.include_router(benefit_routes.router)
app.include_router(visit_routes.router)
app.include_router(assistance_drive_routes.router)


@app.get("/api")
async def api_root():
    """API root endpoint."""
    return {
        "message": "Barangay Senior & PWD Support Tracker API",
        "version": "1.0.0",
        "endpoints": {
            "seniors": "/api/seniors",
            "pwds": "/api/pwds",
            "benefits": "/api/benefits",
            "visits": "/api/visits",
            "assistance_drives": "/api/assistance-drives"
        }
    }

