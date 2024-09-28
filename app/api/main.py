from fastapi import APIRouter

from app.api.routes import (
    schools
)

api_router = APIRouter()

api_router.include_router(schools.router, prefix="/schools", tags=["schools"])
