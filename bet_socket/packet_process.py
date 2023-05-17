
from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession
from bet_socket.protocol import BetProtocol_Response, Req_LoginBetServer, Res_LoginBetServer
from bet_socket.socket_manager import SOCKET_MANAGER, UserSocket
from common.database.model.mongo import Mongo
from redis.asyncio.client import Pipeline
from common.enums import ErrorType, HandlerTopic
from common.logger import LOG
from router.v1.validator.dependencies import DecodeBetToken


async def UserFirstLogin(ws:WebSocket):
    
    try:
        res = Res_LoginBetServer()
        data = await ws.receive_json()
        
        req:Req_LoginBetServer = Req_LoginBetServer(**data)
        
        # token parsing
        userTokenInfo, exp = DecodeBetToken(req.access_token)
        uid = userTokenInfo.uid
        
        await SOCKET_MANAGER.Add(uid, ws, req.access_token)        
        await ws.send_json(res.json())
        
        isSuccess = True
        while isSuccess:
            isSuccess = await SOCKET_MANAGER.Recv(uid)
    except WebSocketDisconnect:
        LOG.d(f'WebSocketDisconnect: {uid}')
        pass
        
    except:
        res.result.SetResult(ErrorType.BET_INVALID_SOCKET_ERROR)
        res.topic = HandlerTopic.BET_NONE.value
        print(res.__dict__)
        await ws.send_json(res.json())
    
    
    
async def UserReLogin(uid:int, data:dict, CDB:AsyncSession, MDB:Mongo, REDIS: Pipeline, s:UserSocket) -> bool:
    
    res = Res_LoginBetServer()
    req = Req_LoginBetServer(**data)
    
    await SOCKET_MANAGER.ReAdd(uid, s, req.access_token)        
    await s.Send(res)
    
    return True