
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


class account_token(MongoDBHeader):
    
    Uid: int
    AccessToken: str
    RefreshToken: str
    
    def __init__(self, Uid, AccessToekn, RefreshToken) -> None:
        super().__init__()
        self.Uid = Uid
        self.AccessToken = AccessToekn
        self.RefreshToken = RefreshToken
