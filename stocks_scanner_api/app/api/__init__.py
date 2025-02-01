"""
API routes initialization.
"""

from fastapi import APIRouter
from app.api.sec import router as sec_router

# Create main router
router = APIRouter()

# Include all route modules
router.include_router(sec_router) 