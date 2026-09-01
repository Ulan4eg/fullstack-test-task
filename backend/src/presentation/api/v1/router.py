from fastapi import APIRouter
from .endpoints import files, alerts

router = APIRouter(prefix="/api/v1")

router.include_router(files.router)
router.include_router(alerts.router)