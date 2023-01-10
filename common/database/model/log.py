
import uuid
from common.gmodel import StructModel
from common.gtime import GTime

class MongoDBHeader(StructModel):
    _id: str
    CreateAt: int
    def __init__(self) -> None:
        super().__init__()
        self._id = str(uuid.uuid4())
        self.CreateAt = int(GTime.UTCStr('%Y%m%d%H%M%S'))

class log_test(MongoDBHeader):
        
    Uid:int
    Nickname:str
    Age:int
    IsTest:bool
    
    def __init__(self, Uid, Nickname, Age, IsTest) -> None:
        super().__init__()
        self.Uid=Uid
        self.Nickname=Nickname
        self.Age=Age
        self.IsTest=IsTest

