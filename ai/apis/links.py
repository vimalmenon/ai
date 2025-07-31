from fastapi import APIRouter

router = APIRouter()


@router.get("/")
def get_links():
    pass


@router.delete("/")
def delete_links():
    pass


@router.post("/")
def update_links():
    pass


@router.put("/")
def create_links():
    pass
