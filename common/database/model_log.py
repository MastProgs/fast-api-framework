
import uuid
from common.gmodel import StructModel
from common.gtime import GTime

class MongoDBHeader(StructModel):
    _id: str
    def __init__(self) -> None:
        super().__init__()
        self._id = GTime.UTCStr('%Y%m%d%H%M%S.') + str(uuid.uuid4())

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

