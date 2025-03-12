from fastapi import APIRouter

from ai.services import S3Service

router = APIRouter()


@router.get("/", tags=["S3"])
async def get_items():
    """Get data from S3 Bucket data"""
    return S3Service().get_items()
