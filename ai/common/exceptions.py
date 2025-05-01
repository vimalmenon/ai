from fastapi import HTTPException


class ClientError(HTTPException):
    """Client error exception."""

    def __init__(self, detail: str, **kwargs):
        super().__init__(status_code=kwargs.get("status_code", 404), detail=detail)


class ServerError(HTTPException):
    """Server error exception."""

    def __init__(self, detail: str, **kwargs):
        super().__init__(status_code=kwargs.get("status_code", 500), detail=detail)
