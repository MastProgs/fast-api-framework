from common.gmodel import Res_WebPacketProtocol, WebPacketProtocol
from common.enums import ErrorType

class AuthProtocol(WebPacketProtocol):
    pass

class Req_Login(AuthProtocol):
    id: str
    pw: str
    
class Res_Login(AuthProtocol, Res_WebPacketProtocol):
    uid: int | None
    access_token: str | None
    refresh_token: str | None    
    
class Req_CreateId(AuthProtocol):
    id: str
    pw: str
    nickname: str
    
    
class Res_CreateId(AuthProtocol, Res_WebPacketProtocol):
    pass


class Req_RefreshToken(AuthProtocol):
    refresh_token: str
    
class Res_RefreshToken(AuthProtocol, Res_WebPacketProtocol):
    access_token: str