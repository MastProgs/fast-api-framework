
import asyncio
import json
from typing import Union
from fastapi import FastAPI, WebSocket, Depends, WebSocketDisconnect

from sqlalchemy.ext.asyncio import AsyncSession
from bet_socket.packet_process import UserFirstLogin, UserReLogin
from bet_socket.protocol import Req_LoginBetServer, Res_LoginBetServer
from bet_socket.socket_manager import SOCKET_MANAGER
from common.database.db import GetCDB, GetMDB, GetRedis
from common.database.model.mongo import Mongo
from redis.asyncio.client import Pipeline

from common.enums import ErrorType, HandlerTopic
from common.logger import LOG

# router description
# https://scshim.tistory.com/575
app = FastAPI(title="Derby Bet Server")

USER_COUNTER = 0

@app.websocket("/ws")
async def WebsocketEndpoint(ws: WebSocket):
    global USER_COUNTER
    await ws.accept()
    
    # Max User Check
    
    USER_COUNTER = USER_COUNTER + 1
    LOG.d(f"User Connected. {USER_COUNTER} users in.")
    
    await UserFirstLogin(ws)
    
    USER_COUNTER = USER_COUNTER - 1
    LOG.d(f"User Disconnected. {USER_COUNTER} users left.")
    
    
    
@app.on_event("startup")
async def Startup(CDB:AsyncSession = Depends(GetCDB), MDB:Mongo = Depends(GetMDB), REDIS: Pipeline = Depends(GetRedis)):
    SOCKET_MANAGER.SetDB(CDB, MDB, REDIS)
    
    # 현재 레이스 정보 season day round 설정 필요
    SOCKET_MANAGER.SetRaceInfo(season=1, day=1, round=1)
    
    # 함수 공통 필수 인자 (uid:int, data:dict, CDB:AsyncSession, MDB:Mongo, REDIS: Pipeline, s:UserSocekt) -> bool
    SOCKET_MANAGER.SetTopic(HandlerTopic.BET_LOGIN.value, UserReLogin)
    pass