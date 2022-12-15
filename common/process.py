
import os
import json

from common.gmodel import Handler, StructModel

class PStatus(StructModel):
    pid: int
    pass

class ProcessStatus(Handler):
        
    fpath: str
    data: PStatus = PStatus()
    #data: dict[str, object] = dict()
    
    def __init__(self, fpath="process_status.json") -> None:
        super().__init__()
        self.fpath = fpath
        self.data.pid = os.getpid()
        
    def FPrint(self, fpath=None):
        if fpath != None:
            self.fpath = fpath
        
        with open(self.fpath, 'w') as outfile:
            json.dump(self.data.__dict__, outfile)
        
    

PS = ProcessStatus()