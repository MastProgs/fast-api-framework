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