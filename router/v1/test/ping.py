
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


from .protocol import ReqTestJson, ResTestJson
@router.post(path="/json"
             , response_model=ResTestJson
             , summary="Test for POST json"
             , description="When need to test json response, then use this post api. response same request data")
async def JsonPost(req: ReqTestJson):
    LOG.d(req)
    return req


from .protocol import Restbl_test
from sqlalchemy.future import select
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.db import GetCDB
from common.database.model_contents import tbl_test

@router.get(path="/dbselect"
            , response_model=Restbl_test
            , summary="Test for DB SELECT api"
            , description="When need to test DB SELECT api, then use this.")
async def DB_select(db:AsyncSession = Depends(GetCDB)):
        
    query = select(tbl_test).where(tbl_test.Nickname == 'abc', tbl_test.IsTest == True).order_by(tbl_test.Uid.desc()).limit(2)
    res = await db.execute(query)
    rowList = res.scalars().fetchall()
    for row in rowList:
        data:tbl_test = row        
        LOG.d(data.__dict__)
        
    return JSONResponse(content=jsonable_encoder(rowList))


@router.get(path="/dbinsert"
            , summary="Test for DB INSERT api"
            , description="When need to test DB INSERT api, then use this.")
async def DB_select(db:AsyncSession = Depends(GetCDB)):
    
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
async def DB_select(db:AsyncSession = Depends(GetCDB)):
    
    query = delete(tbl_test)
    await db.execute(query)
    try:
        await db.commit()
    except:
        await db.rollback()
        msg = f'DB DELETE test failed.'
        LOG.e(msg)
        raise RuntimeError(msg)