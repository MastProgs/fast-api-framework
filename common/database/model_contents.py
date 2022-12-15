
from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, TEXT, BIGINT

CONTENTS_BASE = declarative_base()

class tbl_test(CONTENTS_BASE):
    
    __tablename__ = 'tbl_test'
        
    Uid = Column(Integer, primary_key=True)
    Nickname = Column(String(45), nullable=False, default='')
    Age = Column(Integer, nullable=False, default=0)
    IsTest = Column(Boolean, nullable=False, default=True)

