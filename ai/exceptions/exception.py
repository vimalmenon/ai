from fastapi import HTTPException


class ServerException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=500, **kwargs)


class DbException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=500, **kwargs)


class LLmException(HTTPException):
    def __init__(self, **kwargs):
        super().__init__(status_code=500, **kwargs)
