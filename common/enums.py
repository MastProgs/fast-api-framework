
from enum import Enum, auto

class ErrorType(Enum):
    SUCCESS = auto()
    FAIL = auto()
    
    DB_RUN_FAILED = auto()
    DB_ALREADY_SAME_KEY = auto()
    DB_INVALID_KEY = auto()
    
    
    
    
from fastapi import HTTPException
EXCEPTION_TOKEN_EXPIRED = HTTPException(status_code=403, detail='token has been expired')
EXCEPTION_INVALID_CLIENT_ACCESS = HTTPException(status_code=400, detail='Invalid Server Access')