from fastapi import Header, HTTPException


async def ValidCheckAuthorization(authorization: str = Header(...)):
    if authorization == None:
        raise HTTPException(status_code=400, detail="authorization header invalid")
    else:
        #print(authorization)
        pass


async def ValidCheckBarneyToken(token: str):
    if not "barney" in token:
        raise HTTPException(status_code=400, detail="No Barney token provided")
    
    
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

ACCESS_TOKEN_EXPIRE_MIN = 30                # 30 minutes
REFRESH_TOKEN_EXPIRE_MIN = 60 * 24 * 7      # 7 days
JWT_ALGORITHM = "HS256"

from common.config.config import CONFIG
from common.config.model import JwtToken
__jwtConfig:JwtToken = CONFIG.GetConfig(JwtToken)

JWT_SECRET_KEY = __jwtConfig.access_key
JWT_REFRESH_SECRET_KEY = __jwtConfig.refresh_key

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


def __DecodeToken(jwtToken: str, secretKey: str, algo: str):
    decoded = jwt.decode(jwtToken, secretKey, algo) 
    return decoded.get('sub'), datetime.utcnow() < datetime.strptime(str(decoded.get('exp')), "%Y%m%d%H%M%S")

def DecodeAccessToken(jwtToken: str) -> tuple[UserInfo, bool]:
    strSub, isExpired = __DecodeToken(jwtToken, JWT_SECRET_KEY, JWT_ALGORITHM)
    if False == isExpired:
        return UserInfo(), isExpired
    
    j = json.loads(strSub)
    return UserInfo(**j), isExpired

def DecodeRefreshToken(jwtToken: str) -> tuple[UserInfo, bool]:
    strSub, isExpired = __DecodeToken(jwtToken, JWT_REFRESH_SECRET_KEY, JWT_ALGORITHM)
    if False == isExpired:
        return UserInfo(), isExpired
    
    j = json.loads(strSub)
    return UserInfo(**j), isExpired