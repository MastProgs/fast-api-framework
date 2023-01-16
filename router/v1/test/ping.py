
import json
from fastapi import APIRouter, Header, HTTPException, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from router.v1.validator.dependencies import ValidCheckAuthorization
from common.logger import LOG

router = APIRouter(prefix="/v1/test"
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
            , dependencies=[Depends(ValidCheckAuthorization)]
            , summary="Test for GET auth-header"
            , description="When need to test auth-header, then use this auth-header test")
async def PingGet(authorization: str = Header(default=None)
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
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.db import GetCDB, GetMDB, GetRedis
from common.database.model.contents import tbl_test

@router.get(path="/dbselect"
            , response_model=Res_tbl_test
            , summary="Test for DB SELECT api"
            , description="When need to test DB SELECT api, then use this.")
async def DB_Select(db:AsyncSession = Depends(GetCDB)):
        
    query = select(tbl_test).where(tbl_test.Nickname == 'abc', tbl_test.IsTest == True).order_by(tbl_test.Uid.desc()).limit(2)
    query = select(tbl_test).where(or_(tbl_test.Uid == 10, tbl_test.Uid == 11, tbl_test.Uid == 12)).order_by(tbl_test.Uid.desc()).limit(2)
    res = await db.execute(query)
    rowList = res.scalars().fetchall()
    for row in rowList:
        data:tbl_test = row        
        LOG.d(data.__dict__)
        
    return JSONResponse(content=jsonable_encoder(rowList))


@router.get(path="/dbinsert"
            , summary="Test for DB INSERT api"
            , description="When need to test DB INSERT api, then use this.")
async def DB_Insert(db:AsyncSession = Depends(GetCDB)):
    
    db.add_all([
        tbl_test(Uid=10, Nickname='abc', Age=20, IsTest=True)
        , tbl_test(Uid=11, Nickname='abc', Age=20, IsTest=True)
        , tbl_test(Uid=12, Nickname='abc', Age=20, IsTest=True)
    ])
    try:
        await db.commit()
    except:
        await db.rollback()
        msg = f'DB INSERT test failed.'
        LOG.e(msg)
        raise RuntimeError(msg)


@router.get(path="/dbdelete"
            , summary="Test for DB DELETE api"
            , description="When need to test DB DELETE api, then use this.")
async def DB_Delete(db:AsyncSession = Depends(GetCDB)):
    
    query = delete(tbl_test)
    await db.execute(query)
    try:
        await db.commit()
    except:
        await db.rollback()
        msg = f'DB DELETE test failed.'
        LOG.e(msg)
        raise RuntimeError(msg)
    
    

from common.database.model.log import log_test
@router.get(path="/ldbinsert"
            , summary="Test for Mongo DB INSERT api"
            , description="When need to test Mongo DB INSERT api, then use this.")
async def DB_LogInsert(LOG_DB = Depends(GetMDB)):
    
    l = log_test(3, "log_test", 11, True)
    LOG.d(l.__dict__)
    LOG_DB.log_test.insert_one(l.__dict__)
    
    

from redis import Redis
@router.post(path="/redis-get-sentinel"
            , summary="Test for Sentinel Redis Get api"
            , description="When need to test redis get, use this this.")
async def PingPost(REDIS: Redis = Depends(GetRedis)):
    
    # Sentinel
    REDIS.select(4)
    state = REDIS.zrange('RANK_TOURNAMENT:2022-10-15:09.00.00:60', 0, -1, withscores=True) #.get('RANK_TOURNAMENT:2022-10-15:09.00.00:60')
    if state is not None:
        for key, val in state:
            print(f'{key}, {val}')    
    REDIS.select(0)
    
    
