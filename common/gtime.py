import inspect
import time
from datetime import datetime

from common.gmodel import Handler

class GTime(Handler):
    def UTC():
        return datetime.utcnow()
    
    def UTCStr(format='%Y-%m-%d %H:%M:%S'):
        return time.strftime(format)    
        

class StopWatch(Handler):
    def __init__(self) -> None:
        super().__init__()
        self.start = time.time()
    
    def Stop(self) -> None:
        self.finish = time.time()
        
    def Duration(self, stop=True) -> None:
        if stop:
            self.Stop()
            
        return self.finish - self.start
    
    def Print(self, stop=True) -> None:
        if stop:
            self.Stop()
            
        print(f'Duration : {self.finish - self.start} sec')
        


def SyncHowLong(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        ret = func(*args, **kwargs)
        end = time.time()
        print(f'DELAY - {func.__module__}.{func.__name__}: {end - start} sec')
        return ret
    return wrapper

def AsyncHowLong(func):
    async def wrapper(*args, **kwargs):
        start = time.time()
        ret = await func(*args, **kwargs)
        end = time.time()
        print(f'DELAY - {func.__module__}.{func.__name__}: {end - start} sec')
        return ret
    return wrapper

def HowLong(func):
    return AsyncHowLong(func) if inspect.iscoroutinefunction(func) else SyncHowLong(func)
