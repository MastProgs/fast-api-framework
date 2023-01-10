
from typing import Union
from fastapi import FastAPI

# router description
# https://scshim.tistory.com/575
app = FastAPI(title="Derby Server")


import router.v1.test.ping
app.include_router(router.v1.test.ping.router)

import router.v1.auth.account
app.include_router(router.v1.auth.account.router)
