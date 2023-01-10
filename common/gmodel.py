

class StructModel:    
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
    result: ErrorInfo = ErrorInfo()

class Handler:
    pass


class UserInfo(StructModel):
    uid: int
    id: str
    pw: str
    nickname: str
    
    def __init__(self, uid=None, id=None, pw=None, nickname=None) -> None:
        super().__init__()
        self.uid = uid
        self.id = id
        self.pw = pw
        self.nickname = nickname
        