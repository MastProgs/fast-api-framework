from common.gmodel import WebPacketProtocol

class PingProtocol(WebPacketProtocol):
    pass

class Req_TestJson(PingProtocol):
    msg: str
    desc: str | None = None
    num: int
    
class Res_TestJson(PingProtocol):
    msg: str
    num: int

class Res_tbl_test(PingProtocol):
    
    Uid:int
    Nickname:str
    Age:int
    IsTest:bool
    
    class Config:
        orm_mode = True
