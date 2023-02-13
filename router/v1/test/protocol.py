from common.gmodel import Res_WebPacketProtocol, WebPacketProtocol

class PingProtocol(WebPacketProtocol):
    pass

class Req_TestJson(PingProtocol):
    msg: str
    desc: str | None = None
    num: int
    
class Res_TestJson(PingProtocol, Res_WebPacketProtocol):
    msg: str
    num: int

class Res_tbl_test(PingProtocol, Res_WebPacketProtocol):
    
    Uid:int
    Nickname:str
    Age:int
    IsTest:bool
    
    class Config:
        orm_mode = True
