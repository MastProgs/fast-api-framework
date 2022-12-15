from common.gmodel import WebPacketProtocol
from pydantic import BaseModel

class PingProtocol(WebPacketProtocol):
    pass

class ReqTestJson(BaseModel, PingProtocol):
    msg: str
    desc: str | None = None
    num: int
    
class ResTestJson(BaseModel, PingProtocol):
    msg: str
    num: int

class Restbl_test(BaseModel, PingProtocol):
    
    Uid:int
    Nickname:str
    Age:int
    IsTest:bool
    
    class Config:
        orm_mode = True
