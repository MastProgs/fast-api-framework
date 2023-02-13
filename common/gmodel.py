

class StructModel:    
    pass
class Handler:
    pass

from pydantic import BaseModel
from common.enums import ErrorType

class ErrorInfo(BaseModel, StructModel):
    success: bool | None = True
    code: int | None = ErrorType.SUCCESS.value
    desc: str | None = ErrorType.SUCCESS.name
    
    def SetResult(self, enum:ErrorType):        
        if enum != None:
            self.success = ErrorType.SUCCESS.value == enum.value
            self.code = enum.value
            self.desc = enum.name

class WebPacketProtocol(BaseModel, StructModel):
    pass    

class Req_WebPacketProtocol(WebPacketProtocol):
    access_token: str = ""
class Res_WebPacketProtocol(WebPacketProtocol):
    result: ErrorInfo = ErrorInfo()

import uuid
from common.gtime import GTime

class MongoDBHeader(StructModel):
    _id: str = None
    CreateAt: int = None
    def __init__(self) -> None:
        super().__init__()
        if self._id == None:
            self._id = str(uuid.uuid4())
            
        if self.CreateAt == None:
            self.CreateAt = int(GTime.UTCStr('%Y%m%d%H%M%S'))

class UserInfo(StructModel):
    '''    
    uid: int
    id: str
    nickname: str
    '''
    uid: int
    id: str
    nickname: str
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
        