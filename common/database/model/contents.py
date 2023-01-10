
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TEXT, BIGINT

from common.gtime import GTime

CONTENTS_BASE = declarative_base()

class tbl_test(CONTENTS_BASE):
    
    __tablename__ = 'tbl_test'
        
    Uid = Column(Integer, primary_key=True)
    Nickname = Column(String(45), nullable=False, default='')
    Age = Column(Integer, nullable=False, default=0)
    IsTest = Column(Boolean, nullable=False, default=True)


class tbl_account(CONTENTS_BASE):
    
    __tablename__ = 'tbl_account'
    
    uid = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(String(45), nullable=False, default='')
    pw = Column(String(45), nullable=False, default='')
    nickname = Column(String(45), nullable=False, default='')
    create_at = Column(String(45), nullable=False, default=GTime.UTCStr())