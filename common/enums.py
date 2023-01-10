
from enum import Enum, auto

class ErrorType(Enum):
    SUCCESS = auto()
    FAIL = auto()
    
    DB_RUN_FAILED = auto()
    DB_ALREADY_SAME_KEY = auto()
    DB_INVALID_KEY = auto()