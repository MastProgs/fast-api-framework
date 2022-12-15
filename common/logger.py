
import os
import logging
import logging.handlers
import traceback

from common.gmodel import Handler
from common.gtime import GTime

class StackTracer(Handler):
    
    stackInfo: list[str] = list()  # (file name, line number, called function)
    
    def __init__(self) -> None:
        stacks = traceback.format_stack()[:-2]
        for stack in stacks:
            if not ".py" in stack:
                continue
            
            slist = stack.split(sep=', in ')
            codes = slist[-1]
            slist = slist[0].split(sep=', line ')
            line = slist[-1]
            slist = slist[0].split(sep='.py')
            fname = slist[0].split(sep='\\')[-1] + '.py'
            
            self.stackInfo.append((fname, line, codes))
        pass
    
    
    def Print(self, func) -> None:
        for info in self.stackInfo:
            func(f'{info[0]}, Line {info[1]}')            
            funcName: str = info[2].split(sep='\n')[1]
            func(f'{funcName}')   

    def Println(self, func) -> None:
        for info in self.stackInfo:
            funcName: str = info[2].split(sep='\n')[1]
            func(f'{info[0]}, Line {info[1]}, {funcName}')
        

class Log(Handler):
    
    logger : logging
    __prefix : str = "Server"
    __logLevel : int = logging.INFO
    
    __bFile : bool = True
    __bConsole : bool = True
    __bDB : bool = True
    __bStackTrace : bool = True
    
    def __init__(self, serverName:str = None, logLevel:str = None) -> None:
        super().__init__()
        
        if serverName != None:
            self.__prefix = serverName
        
        if logLevel != None:
            logLevel = logLevel.upper()
            if logging._nameToLevel[logLevel] != None:                
                self.__logLevel = logging._nameToLevel[logLevel]
        
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(self.__logLevel)
                        
        logDir = "./logs"
        if not os.path.exists(logDir):
            os.mkdir(logDir)
        
        # https://docs.python.org/3.11/library/logging.handlers.html#timedrotatingfilehandler
        timedFileHandler = logging.handlers.TimedRotatingFileHandler(filename=logDir + f"/{self.__prefix}.log", utc=True, when='M', interval=10, encoding='utf8')
        timedFileHandler.suffix = "%Y-%m-%dT%H_%M_%S.log"
        
        #formatter = logging.Formatter('%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] %(message)s')
        formatter = logging.Formatter('%(levelname)s => %(message)s')
        timedFileHandler.setFormatter(formatter)
        
        self.logger.addHandler(timedFileHandler)        
        
    
    def d(self, *args, **kwargs) -> None:
        msg = [str(i) for i in list(args)]
        for k, d in kwargs.items():
            msg += f'{str(k)}={str(d)}'
        
        if self.__bFile:
            self.logger.debug(f'[{GTime.UTCStr()}] DEBUG - {str(msg)}')
            
        if self.__bConsole:
            print(f'\033[96mDEBUG\033[0m - [\033[32m{GTime.UTCStr()}\033[0m] \033[93m{str(msg)}\033[0m')
        
    def i(self, *args, **kwargs) -> None:
        msg = [str(i) for i in list(args)]
        for k, d in kwargs.items():
            msg += f'{str(k)}={str(d)}'
            
        if self.__bFile:
            self.logger.info(f'[{GTime.UTCStr()}] INFO - {str(msg)}')
            
        if self.__bConsole:
            print(f'\033[96mINFO\033[0m - [\033[32m{GTime.UTCStr()}\033[0m] \033[93m{str(msg)}\033[0m')
    
    def w(self, *args, **kwargs) -> None:
        msg = [str(i) for i in list(args)]
        for k, d in kwargs.items():
            msg += f'{str(k)}={str(d)}'
            
        if self.__bFile:
            self.logger.warning(f'[{GTime.UTCStr()}] ERROR - {str(msg)}')
                    
        if self.__bConsole:
            print(f'\033[95mWARNING\033[0m - [\033[32m{GTime.UTCStr()}\033[0m] \033[93m{str(msg)}\033[0m')
        
    def e(self, *args, **kwargs) -> None:
        msg = [str(i) for i in list(args)]
        for k, d in kwargs.items():
            msg += f'{str(k)}={str(d)}'
            
        if self.__bStackTrace:
            stackTracer = StackTracer()
                
        if self.__bFile:
            self.logger.error(f'[{GTime.UTCStr()}] ERROR - {str(msg)}')
            if self.__bStackTrace:
                stackTracer.Print(self.logger.error)
                    
        if self.__bConsole:
            if self.__bStackTrace:
                stackTracer.Print(print)
            print(f'\033[31mERROR\033[0m - [\033[32m{GTime.UTCStr()}\033[0m] \033[93m{str(msg)}\033[0m')            
        
    def c(self, *args, **kwargs) -> None:        
        msg = [str(i) for i in list(args)]
        for k, d in kwargs.items():
            msg += f'{str(k)}={str(d)}'
            
        if self.__bStackTrace:
            stackTracer = StackTracer()
            
        if self.__bFile:            
            self.logger.critical(f'[{GTime.UTCStr()}] {str(msg)}')
            if self.__bStackTrace:
                stackTracer.Print(self.logger.critical)
            
        if self.__bConsole:
            if self.__bStackTrace:
                stackTracer.Print(print)
            print(f'\033[31mCRITICAL ERROR\033[0m - [\033[32m{GTime.UTCStr()}\033[0m] \033[93m{str(msg)}\033[0m')            
    
    pass



from common.config.config import CONFIG
from common.config.model import ServerConfig, LogConfig
configInfo: ServerConfig = CONFIG.GetConfig(ServerConfig)
configLog: LogConfig = CONFIG.GetConfig(LogConfig)

LOG = Log(serverName=configInfo.server_name, logLevel=configLog.log_level)