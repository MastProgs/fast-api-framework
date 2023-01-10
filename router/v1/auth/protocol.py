from common.gmodel import WebPacketProtocol
from common.enums import ErrorType


class AuthProtocol(WebPacketProtocol):
    pass
    
class Req_Login(AuthProtocol):
    id: str
    pw: str
    
class Res_Login(AuthProtocol):
    uid: int | None
    access_token: str | None
    refresh_token: str | None    
    
class Req_CreateId(AuthProtocol):
    id: str
    pw: str
    nickname: str
    
    
class Res_CreateId(AuthProtocol):
    pass