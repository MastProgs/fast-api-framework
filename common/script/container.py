
import os
import pandas

from common.gmodel import Handler
from common.logger import LOG
from .models.model import *

class ScriptLibrary(Handler):
    
    __fileExtention = ".xlsx"
    __path: str = ""
    __autoCodeGenPath: str = ""
    
    # __dataLib 는 먼저 DataScript 모델 이름(xlsx 파일 제목) 이 1차적 key 가 되고,
    # 그 다음 커스텀으로 정의한 key 값이 데이터 찾는 key 가 됨.
    #  정의한 key 가 없으면 임의의 index 번호가 key 값이 됨
    __dataLib: dict[str, dict[object, DataScript]] = dict()
    __xlsxSet: set[str] = set()
    
    def __init__(self, path, fileExtention, codeGeneratePath) -> None:
        super().__init__()
        self.__path = path     
        self.__fileExtention = fileExtention
        self.__autoCodeGenPath = codeGeneratePath
        self.__xlsxSet = self.GetXlsxList()
        
    def GetXlsxList(self, path=None, fileExtention=None) -> set[str]:
        if path != None:
            self.__path = path
            
        if fileExtention != None:
            self.__fileExtention = fileExtention
            
        flist = os.listdir(path=self.__path)        
        flist = [fname for fname in flist if self.__fileExtention in fname]
        flist = [fname.split(sep='.')[0] for fname in flist]
        flist = set((fname for fname in flist if fname.isalpha()))
        return flist
        
    def Get(self, cType:type, key=None):
        
        cTypeDict = self.__dataLib.get(cType.__name__)      
        if key == None:
            return cTypeDict
          
        return cTypeDict.get(key)
    
    def ImportDataScript(self, obj:DataScript) -> bool:
        
        if isinstance(obj, DataScript):            
            tName = obj.__class__.__name__
            keyCol = obj.GetKeyCol()
            if "" != keyCol:
                keyVal = getattr(obj, keyCol)
                
                elemDict = self.__dataLib.get(tName)
                if elemDict == None:                    
                    elemDict = dict()
                    self.__dataLib[tName] = elemDict
                    
                elemObj = elemDict.get(keyVal)
                if elemObj == None:
                    elemDict[keyVal] = obj
                    return True
                
                arrCols = obj.GetArrayCols()
                if 0 < len(arrCols):
                    for arrCol in arrCols:
                        arrVal:list = getattr(elemObj, arrCol)
                        objArrVal = getattr(obj, arrCol)
                        arrVal += objArrVal
                        setattr(elemObj, arrCol, arrVal)
                    return True
        
        return False    
        
    def ImportData(self) -> bool:
        
        for data in GetDataList():
            if False == self.ImportDataScript(data):
                LOG.e(f"Init DataScript FAILED.")
                return False
        
        LOG.i(f"Init DataScript SUCCESS.")
        return True

    def IsValid(self, typeName: str) -> bool:
        
        dataLib = self.__dataLib.get(typeName)
        if dataLib == None:
            LOG.w(f"Valid check failed. No Data Imported DataScript Type:{typeName}")
            return False
        
        if typeName == TestExcelData.__name__:
            testExcelContainer: dict[int, TestExcelData] = dataLib
            for key, obj in testExcelContainer.items():
                LOG.d(obj.__dict__)
            
            return True
        
        return True
    
    def ValidCheck(self) -> bool:        
        for cTypeStr in self.__xlsxSet:
            if False == self.IsValid(cTypeStr):
                return False            
        return True

DATA_LIB = ScriptLibrary(path="./xlsx", fileExtention=".xlsx", codeGeneratePath="./common/script/models")

if False == DATA_LIB.ImportData():
    raise RuntimeError()