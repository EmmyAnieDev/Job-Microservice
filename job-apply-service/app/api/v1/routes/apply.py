import logging

from fastapi import APIRouter

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs/apply", tags=["Apply"])

@router.get("")
async def apply():
    return "message: job applied"