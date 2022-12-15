
# pip install fastapi
# pip install "uvicorn[standard]"
# pip install sqlalchemy
# pip install pandas

# Run Server
# python main.py
## if run server in VSCode, then click F5 key in main.py

# Run Server with cmd line --> cd router
# uvicorn router:app --reload --host=0.0.0.0 --port=8000

import uvicorn
import router.router

import unittest
import unit_test

from common.process import PS
PS.FPrint()

from common.config.config import CONFIG
from common.config.model import ServerConfig
configInfo:ServerConfig = CONFIG.GetConfig(ServerConfig)

if configInfo.code_generate_before_run:
    from auto_code_generator import AUTO_MakeDataScriptFiles
    AUTO_MakeDataScriptFiles(xlsxPath="./xlsx", autoCodeGenPath="./common/script/models", outPyFileName="model", readFileExtention=".xlsx")

from common.logger import LOG
from common.script.container import DATA_LIB
LOG.d(DATA_LIB.ValidCheck())


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromModule(unit_test)
    unitTestRes = unittest.TextTestRunner(verbosity=2).run(suite)
    if unitTestRes.wasSuccessful():
        
        
        uvicorn.run(router.router.app, host="0.0.0.0", port=configInfo.port)        
        
    else:
        LOG.e("Unit Test Failed.")