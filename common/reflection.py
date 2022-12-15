
import inspect

from common.gmodel import Handler


# Reflection 사용 시, 초기화가 안되어있거나, None 으로 셋팅되어 있는 경우, 메모리 할당이 안되어 있어서 정상적으로 값을 못불러옴
class Reflection(Handler):
    
    def GetClassMemberName(cls: object) -> list[str]:
        ret: list[str] = []
        for mem in inspect.getmembers(cls):
            if not mem[0].startswith('_'):
                if not inspect.ismethod(mem[1]):
                    ret.append(mem[0])
        
        return ret
    
    def GetClassMemberType(cls: object) -> list[type]:
        ret: list[type] = []
        for mem in inspect.getmembers(cls):
            if not mem[0].startswith('_'):
                if not inspect.ismethod(mem[1]):
                    val = getattr(cls, mem[0])
                    ret.append(type(val))
        
        return ret
    
    def GetClassMemberValue(cls: object) -> list:
        ret = list()
        for mem in inspect.getmembers(cls):
            if not mem[0].startswith('_'):
                if not inspect.ismethod(mem[1]):
                    val = getattr(cls, mem[0])
                    ret.append(val)
        
        return ret
    
    pass