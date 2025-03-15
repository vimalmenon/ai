from pydantic import BaseModel


class S3Item(BaseModel):
    name: str
    size: int
    last_modified: str


class S3Request(BaseModel):
    name: str
    data: str
