from asyncio import current_task
from common.database.model_contents import CONTENTS_BASE

from common.config.config import CONFIG
from common.config.model import ContentsDBConfig, LogDBConfig
from enum import Enum, auto

from common.gmodel import Handler
from common.logger import LOG

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_scoped_session
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient

__DB_URL_MAP = {
    "mysql":"mysql+asyncmy"
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
__CDB_ENGINE = create_async_engine(__CDB_URL, echo=__cdbInfo.show_log)
__CDB_ASYNC_SESSION = async_scoped_session(sessionmaker(__CDB_ENGINE, class_=AsyncSession, expire_on_commit=False, autocommit=False), scopefunc=current_task)


__ldbInfo:LogDBConfig = CONFIG.GetConfig(LogDBConfig)
# __LDB_URL = f'{__DB_URL_MAP[__ldbInfo.db_type]}://{__ldbInfo.id}:{__ldbInfo.pw}@{__ldbInfo.host}:{__ldbInfo.port}/{__ldbInfo.name}'
# if __ldbInfo.id == '':
#     __CDB_URL = f'{__DB_URL_MAP[__ldbInfo.db_type]}://{__ldbInfo.host}:{__ldbInfo.port}/{__ldbInfo.name}'
# elif __ldbInfo.pw == '':
#     __CDB_URL = f'{__DB_URL_MAP[__ldbInfo.db_type]}://{__ldbInfo.id}@{__ldbInfo.host}:{__ldbInfo.port}/{__ldbInfo.name}'
# __LDB_ENGINE = create_async_engine(__LDB_URL, echo=__ldbInfo.show_log)
# __LDB_ASYNC_SESSION = async_scoped_session(sessionmaker(__LDB_ENGINE, class_=AsyncSession, expire_on_commit=False, autocommit=False), scopefunc=current_task)
__LOG_DB = MongoClient(host=__ldbInfo.host, port=__ldbInfo.port)


async def __InitModel():
    async with __CDB_ENGINE.begin() as conn:
        #await conn.run_sync(CONTENTS_BASE.metadata.drop_all)
        await conn.run_sync(CONTENTS_BASE.metadata.create_all)
    
        
async def GetCDB() -> AsyncSession:
    async with __CDB_ASYNC_SESSION() as s:
        yield s

async def GetLDB():
    return __LOG_DB[__ldbInfo.name]
