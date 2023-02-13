
from common.gmodel import MongoDBHeader

class log_test(MongoDBHeader):
    '''
    Uid :int
    Nickname :str
    Age :int
    IsTest :bool
    '''    
    Uid :int
    Nickname :str
    Age :int
    IsTest :bool
    
    def __init__(self, *args, **kwargs) -> None:
        for dictionary in args:
            for key in dictionary:
                setattr(self, key, dictionary[key])
        for key in kwargs:
            setattr(self, key, kwargs[key])
        super().__init__()
