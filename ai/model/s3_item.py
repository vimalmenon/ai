from pydantic import BaseModel


class S3Item(BaseModel):
    name: str
    size: int
    last_modified: str
