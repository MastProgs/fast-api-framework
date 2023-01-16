
from fastapi import APIRouter, Header, HTTPException, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.db import GetCDB, GetMDB
from sqlalchemy.future import select
from sqlalchemy import delete, or_
from common.gmodel import UserInfo
from router.v1.validator.dependencies import DecodeAccessToken, ValidCheckAuthorization, CreateAccessToken, CreateRefreshToken
from common.logger import LOG
from common.enums import ErrorType



router = APIRouter(prefix="/v1/auth"
                   , tags=["Auth"]
                   , responses = { 404: {"description": "Not found"}})

from .protocol import Req_Login, Res_Login
from common.database.model.contents import tbl_account
@router.post(path="/login"
            , response_model=Res_Login
            , summary="Request login access"
            , description="Do login process")
async def Login(req: Req_Login, db:AsyncSession = Depends(GetCDB), mdb = Depends(GetMDB)):
        
    query = select(tbl_account).where(tbl_account.id == req.id, tbl_account.pw == req.pw).limit(1)
    res = await db.execute(query)
    rowList = res.scalars().fetchall()
    
    ret = Res_Login()
    if 1 != len(rowList):
        ret.result.SetResult(ErrorType.DB_INVALID_KEY)
        return ret
    
    for row in rowList:
        data:tbl_account = row
        ret.uid = data.uid
        break
    
    ret.access_token = CreateAccessToken(UserInfo(uid=ret.uid, id=req.id, nickname=data.nickname))
    ret.refresh_token = CreateRefreshToken(UserInfo(uid=ret.uid, id=req.id, nickname=data.nickname))
    
    ui = DecodeAccessToken(ret.access_token)
    LOG.d(ui.__dict__)
    
    return ret


from .protocol import Req_CreateId, Res_CreateId
@router.post(path="/create"
            , response_model=Res_CreateId
            , summary="Request create ID"
            , description="Make new id")
async def CreateId(req: Req_CreateId, db:AsyncSession = Depends(GetCDB), mdb = Depends(GetMDB)):
    
    query = select(tbl_account).where(tbl_account.id == req.id).limit(1)
    res = await db.execute(query)
    rowList = res.scalars().fetchall()
    
    ret = Res_CreateId()
    if len(rowList):
        ret.result.SetResult(ErrorType.DB_ALREADY_SAME_KEY)
        return ret        
    
    db.add(tbl_account(id=req.id, pw=req.pw, nickname=req.nickname))
    
    try:
        await db.commit()
    except:
        await db.rollback()
        msg = f'DB INSERT test failed.'
        LOG.e(msg)
        ret.result.SetResult(ErrorType.DB_RUN_FAILED)
        return ret   
    
    return ret