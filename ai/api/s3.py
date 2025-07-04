from fastapi import APIRouter

from ai.model import S3Request
from ai.services import S3Service

router = APIRouter()


@router.get("", tags=["S3"])
async def get_items():
    """Get data from S3 Bucket data"""
    return {"data": S3Service().get_items()}


@router.get("/read_item/{item}", tags=["S3"])
async def read_items(item: str):
    """Read the data based on item key provided"""
    return {"data": S3Service().read_item(item)}


@router.post("/upload_item", tags=["S3"])
async def upload_item(data: S3Request):
    return {"data": S3Service().upload_item(data)}


@router.post("/sync", tags=["S3"])
async def sync_bucket():
    """Sync the data to Table"""
    return {"data": S3Service().sync_bucket()}


@router.delete("/delete_item/{item}", tags=["S3"])
async def delete_item(item: str):
    """Delete the item from S3 Bucket"""
    return {"data": S3Service().delete_item(item)}
