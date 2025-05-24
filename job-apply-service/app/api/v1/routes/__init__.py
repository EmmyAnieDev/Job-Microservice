from fastapi import APIRouter
from app.api.v1.routes.apply import router as apply_router

router = APIRouter(prefix="/v1")
router.include_router(apply_router)