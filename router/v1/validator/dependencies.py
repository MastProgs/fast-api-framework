from fastapi import Header, HTTPException
from common.enums import EXCEPTION_INVALID_CLIENT_ACCESS, EXCEPTION_TOKEN_EXPIRED


async def ValidCheckAuthorization(authorization: str = Header(...)):
    if authorization == None:
        raise HTTPException(status_code=400, detail="authorization header invalid")
    else:
        #print(authorization)
        pass


async def ValidCheckBarneyToken(token: str):
    if not "barney" in token:
        raise HTTPException(status_code=400, detail="No Barney token provided")
    

from common.config.config import CONFIG
from common.config.model import ServerConfig
async def IsChatServer():    
    sc:ServerConfig = CONFIG.GetConfig(ServerConfig)    
    if False == sc.is_chat:
        raise EXCEPTION_INVALID_CLIENT_ACCESS

async def IsWebServer():    
    sc:ServerConfig = CONFIG.GetConfig(ServerConfig)    
    if True == sc.is_chat:
        raise EXCEPTION_INVALID_CLIENT_ACCESS
    
    
from passlib.context import CryptContext
__pwContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def GetHashedPW(pw: str) -> str:
    return __pwContext.hash(pw)

def VerifyPW(pw: str, hashedPass: str) -> bool:
    return __pwContext.verify(pw, hashedPass)


import uuid
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from common.gmodel import UserInfo


from common.config.model import JwtToken
__jwtConfig:JwtToken = CONFIG.GetConfig(JwtToken)

JWT_SECRET_KEY = __jwtConfig.access_key
JWT_REFRESH_SECRET_KEY = __jwtConfig.refresh_key
ACCESS_TOKEN_EXPIRE_MIN = __jwtConfig.access_expire_min             # 30 minutes
REFRESH_TOKEN_EXPIRE_MIN = 60 * 24 * __jwtConfig.refresh_expire_day # 7 days
JWT_ALGORITHM = "HS256"

def __CreateToken(subject: Union[str, Any], secretKey:str, algo:str, expireMin: int, expiresDelta: str = None):    
    
    if expiresDelta is not None:
        expDt = datetime.strptime(expiresDelta, "%Y%m%d%H%M%S")
        expDt = datetime.utcnow() + expDt
    else:
        expDt = datetime.utcnow() + timedelta(minutes=expireMin)
    
    toEncode = {"exp": int(expDt.strftime("%Y%m%d%H%M%S")), "sub": str(subject)}
    encodedJWT = jwt.encode(toEncode, secretKey, algo)
    return encodedJWT
    

import json
def CreateAccessToken(subject: UserInfo, expiresDelta: str = None) -> str:
    return __CreateToken(json.dumps(subject.__dict__), JWT_SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MIN, expiresDelta)

def CreateRefreshToken(subject: UserInfo, expiresDelta: str = None) -> str:
    return __CreateToken(json.dumps(subject.__dict__), JWT_REFRESH_SECRET_KEY, JWT_ALGORITHM, REFRESH_TOKEN_EXPIRE_MIN, expiresDelta)


def __DecodeToken(jwtToken: str, secretKey: str, algo: str) -> tuple[str, bool, str]:
    decoded = jwt.decode(jwtToken, secretKey, algo)
    expireDt = str(decoded.get('exp'))
    return decoded.get('sub'), datetime.utcnow() < datetime.strptime(expireDt, "%Y%m%d%H%M%S"), expireDt

def DecodeAccessToken(jwtToken: str) -> tuple[UserInfo, str]:
    strSub, isNotExpired, expireDt = __DecodeToken(jwtToken, JWT_SECRET_KEY, JWT_ALGORITHM)
    if False == isNotExpired:
        raise EXCEPTION_TOKEN_EXPIRED
    
    j = json.loads(strSub)
    return UserInfo(**j), expireDt

def DecodeRefreshToken(jwtToken: str) -> tuple[UserInfo, str]:
    strSub, isNotExpired, expireDt = __DecodeToken(jwtToken, JWT_REFRESH_SECRET_KEY, JWT_ALGORITHM)
    if False == isNotExpired:
        raise EXCEPTION_TOKEN_EXPIRED
    
    j = json.loads(strSub)
    return UserInfo(**j), expireDt