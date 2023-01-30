
from fastapi import APIRouter, Header, HTTPException, Depends, Response
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.db import GetCDB, GetMDB
from sqlalchemy.future import select
from sqlalchemy import delete, or_
from common.gmodel import UserInfo
from router.v1.validator.dependencies import DecodeAccessToken, DecodeRefreshToken, IsChatServer, IsWebServer, ValidCheckAuthorization, CreateAccessToken, CreateRefreshToken
from common.logger import LOG
from common.enums import ErrorType



router = APIRouter(prefix="/v1/auth"
                   , tags=["Auth"]
                   , responses = { 404: {"description": "Not found"}})

from .protocol import Req_Login, Req_RefreshToken, Res_Login, Res_RefreshToken
from common.database.model.contents import tbl_account
@router.post(path="/login"
            , dependencies=[Depends(IsWebServer)]
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
    
    ui, expDt = DecodeAccessToken(ret.access_token)
    LOG.d(ui.__dict__)
    
    return ret


from .protocol import Req_CreateId, Res_CreateId
@router.post(path="/create"
            , dependencies=[Depends(IsWebServer)]
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


@router.post(path="/refresh_token"
            , dependencies=[Depends(IsWebServer)]
            , response_model=Res_RefreshToken
            , summary="refresh login access token"
            , description="when access token was despired. refresh access token use with refresh token.")
async def Login(req: Req_RefreshToken):
    
    rft, expDt = DecodeRefreshToken(req.refresh_token)
    ret = Res_RefreshToken(access_token=CreateAccessToken(rft))
    return ret