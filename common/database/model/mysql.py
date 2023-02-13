
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TEXT, BIGINT

from common.gtime import GTime

CONTENTS_BASE = declarative_base()

class tbl_test(CONTENTS_BASE):
    
    __tablename__ = 'tbl_test'
        
    uid = Column(Integer, primary_key=True)
    nickname = Column(String(45), nullable=False, default='')
    age = Column(Integer, nullable=False, default=0)
    is_test = Column(Boolean, nullable=False, default=True)


class tbl_account(CONTENTS_BASE):
    
    __tablename__ = 'tbl_account'
    
    uid = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(45), nullable=False)
    pw = Column(String(45), nullable=False, default='')
    nickname = Column(String(45), nullable=False)
    create_at = Column(String(45), nullable=False, default=GTime.UTCStr())

    def ToJson(self) -> str:
        return str({"uid" : self.uid, "id": self.id, "pw": self.pw, "nickname": self.nickname, "create_at": self.create_at})
    