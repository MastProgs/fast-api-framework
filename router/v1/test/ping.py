
import json
from fastapi import APIRouter, Header, HTTPException, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from common.config.config import CONFIG
from common.config.model import ContentsDBConfig
from common.dice import Dice, DiceElem, DiceExclude
from common.enums import ErrorType
from common.gmodel import RaceEntryInfo, Res_WebPacketProtocol
from common.script.container import DATA_LIB
from common.script.models.model import JockeyData, LineageData, RaceTrackData, RacingScheduleTable, StringHorseFirstName, StringHorseLastName
from contents.horse.status import Genealogy, MakeNewHorse, CalculateRestoreHorseStamina, MakeNewHorse
from contents.pilot.status import MakeNewPilot
from contents.race.result import InsertRaceResultRecord, NewRaceTrackRecord
from router.v1.validator.dependencies import IsDevTest, TEST_ValidCheckAuthorization
from common.logger import LOG
from common.database.redis_handler import KeyMaker
from redis.asyncio import Redis
from redis.asyncio.client import Pipeline

router = APIRouter(prefix="/v1/test"
                   , dependencies=[Depends(IsDevTest)]
                   , tags=["Test"]
                   , responses = { 404: {"description": "Not found"}})


@router.get(path="/ping"
            , summary="Test for GET api"
            , description="When need to test get api, then use this get ping test")
async def PingGet():
    return "pong"


@router.post(path="/ping"
            , summary="Test for POST api"
            , description="When need to test post api, then use this post ping test")
async def PingPost():
    return "post_pong"


@router.get(path="/auth-header"
            , dependencies=[Depends(TEST_ValidCheckAuthorization)]
            , summary="Test for GET auth-header"
            , description="When need to test auth-header, then use this auth-header test")
async def AuthHeader(authorization: str = Header(default=None)
                  , token: str = Header(default=None)):
    LOG.d(authorization, token)
    return "success"


from .protocol import Req_TestJson, Res_TestJson
@router.post(path="/json"
             , response_model=Res_TestJson
             , summary="Test for POST json"
             , description="When need to test json response, then use this post api. response same request data")
async def JsonPost(req: Req_TestJson):
    LOG.d(req)
    return req


from .protocol import Res_tbl_test
from sqlalchemy.future import select
from sqlalchemy import delete, or_
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.db import CDBExcute, CDBJob_Add, CDBRun, GetCDB, GetMDB, GetMDB_Session, GetRedis
from common.database.model.mysql import tbl_horse_best_record, tbl_horse_score, tbl_horse_status, tbl_pilot_score, tbl_pilot_status, tbl_race_horse_record, tbl_race_track_record, tbl_test

@router.get(path="/dbselect"
            , response_model=Res_tbl_test
            , summary="Test for DB SELECT api"
            , description="When need to test DB SELECT api, then use this.")
async def DB_Select(db:AsyncSession = Depends(GetCDB)):
        
    query = select(tbl_test).where(tbl_test.nickname == 'abc', tbl_test.is_test == True).order_by(tbl_test.uid.desc()).limit(2)
    #query = select(tbl_test).where(or_(tbl_test.uid == 10, tbl_test.uid == 11, tbl_test.uid == 12)).order_by(tbl_test.uid.desc()).limit(2)
    #query = select(tbl_test).where(tbl_test.uid == [10, 11, 12]).order_by(tbl_test.uid.desc()).limit(2)
    
    
    # res = await db.execute(query)
    # rowList = res.scalars().fetchall()
    # print(hasattr(res, 'scalars'), hasattr(res, 'fetchall'), hasattr(res, 'rowcount'))
    
    
    errType, rowList = await CDBExcute(db, query)       
    if errType != ErrorType.SUCCESS:
        raise RuntimeError(errType.name)
    
    for row in rowList:
        data:tbl_test = row        
        LOG.d(data.__dict__)
        
    return JSONResponse(content=jsonable_encoder(rowList))


@router.get(path="/dbinsert"
            , summary="Test for DB INSERT api"
            , description="When need to test DB INSERT api, then use this.")
async def DB_Insert(db:AsyncSession = Depends(GetCDB)):
    
    db.add_all([
        tbl_test(uid=10, nickname='abc', age=20, is_test=True)
        , tbl_test(uid=11, nickname='abc', age=20, is_test=True)
        , tbl_test(uid=12, nickname='abc', age=20, is_test=True)
    ])
    
    errType = await CDBRun(db, 'DB INSERT test failed.')
    if errType != ErrorType.SUCCESS:
        raise RuntimeError(errType.name)
    


@router.get(path="/dbdelete"
            , summary="Test for DB DELETE api"
            , description="When need to test DB DELETE api, then use this.")
async def DB_Delete(db:AsyncSession = Depends(GetCDB)):
    
    errType, rowList = await CDBExcute(db, delete(tbl_test), 'DB DELETE test failed.')
    if errType != ErrorType.SUCCESS:
        raise RuntimeError(errType.name)
    
    
# mongo db example
# https://www.w3schools.com/python/python_mongodb_insert.asp 
from common.database.model.mongo import Mongo
@router.get(path="/ldbinsert"
            , summary="Test for Mongo DB INSERT api"
            , description="When need to test Mongo DB INSERT api, then use this.")
async def DB_LogInsert(MDB:Mongo = Depends(GetMDB)):
    
    async with await GetMDB_Session() as s:        
            
        try:            
            s.start_transaction()
        
            l = Mongo.log_test(Uid=3, Nickname="log_test", Age=11, IsTest=True)
            LOG.d(l.__dict__)
            await MDB.log_test.insert_one(l.__dict__)
            
            s.commit_transaction()
        except Exception:
            s.abort_transaction()
        
    
    # l = Mongo.log_test(Uid=3, Nickname="log_test", Age=11, IsTest=True)
    # LOG.d(l.__dict__)
    # await MDB.log_test.insert_one(l.__dict__)
    return
    
@router.get(path="/ldbselect"
            , summary="Test for Mongo DB SELECT api"
            , description="When need to test Mongo DB INSERT api, then use this.")
async def DB_LogSelect(MDB:Mongo = Depends(GetMDB)):    
        
    res = await MDB.log_test.find().sort('CreateAt', -1).limit(2).to_list(length=2)
    for d in res:
        LOG.d(d)
    
    return res


from redis import Redis
@router.get(path="/redis-get-sentinel"
            , summary="Test for Sentinel Redis Get api"
            , description="When need to test redis get, use this this.")
async def RedisGetSentinel(REDIS: Pipeline = Depends(GetRedis)):
    
    # Sentinel
    await REDIS.select(4)
    state = await REDIS.zrange('RANK_TOURNAMENT:2022-10-15:09.00.00:60', 0, -1, withscores=True) #.get('RANK_TOURNAMENT:2022-10-15:09.00.00:60')
    if state is not None:
        for key, val in state:
            print(f'{key}, {val}')    
    await REDIS.select(0)
    
