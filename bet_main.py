
import uvicorn
import bet_socket.router

from common.config.config import CONFIG
from common.config.model import BetServerConfig
configInfo:BetServerConfig = CONFIG.GetConfig(BetServerConfig)

from common.logger import LOG
from common.script.container import DATA_LIB
IS_VALID_DATA_SCRIPTS = DATA_LIB.ValidCheck()
if IS_VALID_DATA_SCRIPTS:
    LOG.d(f'Script Data Valid Check Successful')


if __name__ == "__main__":
    uvicorn.run(bet_socket.router.app, host="0.0.0.0", port=configInfo.port)  