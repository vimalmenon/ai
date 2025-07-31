from fastapi import APIRouter

from ai.model import LinkGroupSlim, LinkSlim
from ai.services import LinkService

router = APIRouter()


@router.get("", tags=["links"])
async def get_links():
    data = LinkService().get_links()
    return {"data": data}


@router.delete("/{id}", tags=["links"], status_code=204)
async def delete_link(id: str):
    LinkService().delete_link(id)


@router.delete("/{lg_id}/{id}", tags=["links"], status_code=204)
async def delete_link_group(lg_id: str, id: str):
    pass


@router.put("", tags=["links"])
async def create_group_link(data: LinkGroupSlim):
    result = LinkService().create_group_link(data)
    return {"data": result}


@router.put("/{id}", tags=["links"])
async def create_link(id: str, data: LinkSlim):
    result = LinkService().create_link(id, data)
    return {"data": result}
