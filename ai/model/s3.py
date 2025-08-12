from typing import Any

from ai.model.base_model import Base


class S3Item(Base):
    name: str
    size: int
    last_modified: str


class S3Request(Base):
    name: str
    data: str


class S3Items:
    name: str
    type: str
    data: Any
    size: int
    created_date: str
    archive: bool
