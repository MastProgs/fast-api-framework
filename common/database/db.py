from asyncio import current_task

from redis import Redis
from common.database.model.mysql import CONTENTS_BASE

from common.config.config import CONFIG
from common.config.model import ContentsDBConfig, MongoDBConfig, RedisConfig
from enum import Enum, auto

from common.gmodel import Handler
from common.logger import LOG

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from redis_om import get_redis_connection

__DB_URL_MAP = {
    "mysql":"mysql+aiomysql"
    #"mysql":"mysql+asyncmy"
    , "mongodb":"mongodb"
}

# asyncio query docs
# https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html 

class DBType(Enum):
    CONTENTS = auto()
    LOG = auto()

__cdbInfo:ContentsDBConfig = CONFIG.GetConfig(ContentsDBConfig)  
__CDB_URL = f'{__DB_URL_MAP[__cdbInfo.db_type]}://{__cdbInfo.id}:{__cdbInfo.pw}@{__cdbInfo.host}:{__cdbInfo.port}/{__cdbInfo.name}'
if __cdbInfo.pw == '':
    __CDB_URL = f'{__DB_URL_MAP[__cdbInfo.db_type]}://{__cdbInfo.id}@{__cdbInfo.host}:{__cdbInfo.port}/{__cdbInfo.name}'
__CDB_ENGINE = create_async_engine(__CDB_URL, echo=__cdbInfo.show_log, pool_size=10, max_overflow=50)
__CDB_ASYNC_SESSION = async_scoped_session(sessionmaker(__CDB_ENGINE, class_=AsyncSession, expire_on_commit=False, autocommit=False), scopefunc=current_task)


__redisInfo: RedisConfig = CONFIG.GetConfig(RedisConfig)
__REDIS = get_redis_connection(
    host=__redisInfo.host,
    port=__redisInfo.port,
    decode_responses=True
)


__mdbInfo:MongoDBConfig = CONFIG.GetConfig(MongoDBConfig)
__MONGO_DB = MongoClient(host=__mdbInfo.host, port=__mdbInfo.port)


async def __InitModel():
    async with __CDB_ENGINE.begin() as conn:
        #await conn.run_sync(CONTENTS_BASE.metadata.drop_all)
        await conn.run_sync(CONTENTS_BASE.metadata.create_all)
    
        
async def GetCDB() -> AsyncSession:
    async with __CDB_ASYNC_SESSION() as s:
        yield s

async def GetMDB():
    return __MONGO_DB[__mdbInfo.name]

async def GetRedis() -> Redis:
    return __REDIS
