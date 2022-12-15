import time
from datetime import datetime

from common.gmodel import Handler

class GTime(Handler):
    def UTC():
        return datetime.now()
    
    def UTCStr():
        return time.strftime('%Y-%m-%d %H:%M:%S')    
        

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
        


def HowLong(func):
    def Wrapper(*args, **kwargs):
        sw = StopWatch()
        ret = func(*args, **kwargs)
        print(f'DELAY - {func.__module__}.{func.__name__}: {sw.Duration()} sec')
        return ret
    
    return Wrapper
