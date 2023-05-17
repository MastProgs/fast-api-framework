
from typing import Union
from fastapi import WebSocket

from bet_socket.protocol import BetProtocol_Request, BetProtocol_Response
from common.enums import HandlerTopic
from common.logger import LOG

from sqlalchemy.ext.asyncio import AsyncSession
from common.database.model.mongo import Mongo
from redis.asyncio.client import Pipeline

from router.v1.validator.dependencies import DecodeBetToken

class UserSocket:
    uid:int = 0
    s:WebSocket = None
    accessToken:str = ""
    
    def __init__(self, uid:int, s:WebSocket, access_token:str):
        self.uid = uid
        self.s = s
        self.accessToken = access_token
        
    def IsTokenSame(self, newToken:str) -> bool:
        return newToken == self.accessToken
        
    async def Send(self, data: BetProtocol_Request):
        await self.s.send_json(data.json())
        
    async def Recv(self) -> dict:
        return await self.s.receive_json()
    
    async def Close(self):
        await self.s.close()
        self.s = None
        self.uid = 0

class SocketManager:
    
    userSocketDict: dict[int, UserSocket] = {}
    packetHandler: dict[int, callable] = {}
    validTopic: set[int] = set()
    
    CDB: AsyncSession = None
    MDB: Mongo = None
    REDIS: Pipeline = None
    
    raceSeason: int = 0
    raceDay: int = 0
    raceRound: int = 0
    racePrepareTimeMinute: int = 0
    
    def __init__(self):
        for e in HandlerTopic:
            if HandlerTopic.BET_NONE.value < e.value < HandlerTopic.BET_MAX.value:
                self.validTopic.add(e.value)        
        
    def __del__(self):
        self.CloseAll()
        
    
    def SetDB(self, CDB:AsyncSession, MDB:Mongo, REDIS: Pipeline):
        self.CDB = CDB
        self.MDB = MDB
        self.REDIS = REDIS
        
    def SetTopic(self, topic:int, func:callable):
        self.packetHandler[topic] = func
        
    def SetRaceInfo(self, season:int, day:int, round:int):
        self.raceSeason = season
        self.raceDay = day
        self.raceRound = round
    
    async def Add(self, uid:int, s:WebSocket, accessToken:str):
        user = self.userSocketDict.get(uid)
        if user != None:
            await self.Close(uid)
        self.userSocketDict[uid] = UserSocket(uid, s, accessToken)
    
    async def ReAdd(self, uid:int, s:WebSocket, accessToken:str):
        user = self.userSocketDict.get(uid)
        if user != None:
            user.accessToken = accessToken
        else:
            LOG.e_no_callstack(f"SocketManager::ReAdd() user is None. uid:{uid}")
            s.close()

    async def Send(self, uid:int, data:BetProtocol_Request):
        user = self.userSocketDict.get(uid)
        if user == None:
            LOG.w(f"SocketManager::send() user is None. uid:{uid}")
            return
        
        await user.Send(data)

    async def Recv(self, uid:int) -> bool:
        userSocket = self.userSocketDict.get(uid)
        if userSocket == None:
            LOG.w(f"SocketManager::recv() user is None. uid:{uid}")
            return False

        data:dict = await userSocket.Recv()
        packetType:int = data.get("topic")
        if packetType == None:
            LOG.e_no_callstack(f"SocketManager::recv() packetType is None. uid:{uid}")
            return False
        
        if packetType not in self.validTopic:
            LOG.e_no_callstack(f"SocketManager::recv() packetType is invalid. uid:{uid}, packetType:{packetType} - {HandlerTopic(packetType).name}")
            return False
        
        token = data.get("access_token")
        if token == None:
            LOG.e_no_callstack(f"SocketManager::recv() token is None. uid:{uid}, packetType:{packetType} - {HandlerTopic(packetType).name}")
            return False
        
        if (not userSocket.IsTokenSame(token)) and (packetType != HandlerTopic.BET_LOGIN.value):
            LOG.e_no_callstack(f"SocketManager::recv() token is invalid. uid:{uid}, packetType:{packetType} - {HandlerTopic(packetType).name}")
            return False
        
        # token check ( season, day, round, uid, token )
        userTokenInfo, exp = DecodeBetToken(token)
        
        # create time check
        userTokenInfo.create_at
        self.racePrepareTimeMinute
        
        if userTokenInfo.race_season != self.raceSeason or userTokenInfo.race_day != self.raceDay or userTokenInfo.race_round != self.raceRound:
            LOG.e_no_callstack(f"SocketManager::recv() token season day round info is invalid. uid:{uid}, packetType:{packetType} - {HandlerTopic(packetType).name}")
            return False        
        
        func = self.packetHandler.get(packetType)
        if func == None:
            LOG.e_no_callstack(f"SocketManager::recv() func is None. uid:{uid}, packetType:{packetType} - {HandlerTopic(packetType).name}")
            return False
        
        if False == await func(uid, data, self.CDB, self.MDB, self.REDIS, userSocket):
            return False
        
        return True
        

    async def Close(self, uid:int):
        
        try:        
            user = self.userSocketDict.pop(uid)
            await user.Close()
            
        except KeyError:
            LOG.w(f"SocketManager::close() user is None. uid:{uid}")
            return
        
        except:
            LOG.e(f"SocketManager::close() error. uid:{uid}")
            return
        
    
    async def CloseAll(self):
        for uid in self.userSocketDict:
            user = self.userSocketDict.get(uid)
            if user != None:
                user.Close()
        
        
    async def Broadcast(self, data:BetProtocol_Request):
        for user in self.userSocketDict.values():
            await user.Send(data)
            
            


SOCKET_MANAGER:SocketManager = SocketManager()

