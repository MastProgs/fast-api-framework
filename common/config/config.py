import tomllib

from common.gmodel import Handler
from common.config.model import *
from common.reflection import Reflection

class Config(Handler):
    
    __configFileName: str
    __parseData: dict[str, object] = dict()
    __objList: dict[str, object] = dict()
    
    def __init__(self, fname:str) -> None:
        self.UpdateConfigFileName(fname)
        self.ParseToml(self.__configFileName)
        
    def UpdateConfigFileName(self, fname:str) -> None:
        self.__configFileName = fname        
                    
    def ParseToml(self, fname=None) -> None:
        if fname != None:
            self.UpdateConfigFileName(fname)
        
        with open(self.__configFileName, "rb") as f:
            self.__parseData = tomllib.load(f)
            
    def ImportForm(self, *args) -> None:
        tl = [i for i in args]
        for t in tl:            
            obj = t()
            if isinstance(obj, ConfigModel):
                
                # 타입을 받았으니, 해당 타입에 맞게 값을 toml 에서 부터 찾아 넣어줘야 함
                memberNameList = Reflection.GetClassMemberName(obj)
                for memberName in memberNameList:
                    try:                        
                        setattr(obj, memberName, self.__parseData[obj.__class__.__name__][memberName])
                    except:
                        errMsg = f"Invalid Config Model Imported. you must import valid member. check config.toml or ConfigModel. Error Type was {obj.__class__.__name__}."
                        #LOG.c(errMsg)
                        raise TypeError(errMsg)                        
                
                self.__objList[obj.__class__.__name__] = obj
            else:
                errMsg = f"Invalid Config Model Imported. you must import only ConfigModel. Error Type was {obj.__class__.__name__}."
                raise TypeError(errMsg)
    
    def GetConfig(self, t: type) -> ConfigModel:
        try:            
            config = self.__objList[t.__name__]
        except:
            errMsg = f"Invalid Config Model Loaded. you must import ConfigModel before GetConfig. Error Type was {t.__name__}."
            raise TypeError(errMsg)
        
        return config

CONFIG = Config(fname="config.toml")
CONFIG.ImportForm(ServerConfig, LogConfig, ContentsDBConfig, LogDBConfig, JwtToken)