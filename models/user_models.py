from datetime import datetime
from xmlrpc.client import Boolean
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    id = Column(Integer,primary_key=True,index=True)
    username =Column(String(110), unique=True, index=True)  
    hashed_password = Column(String(255))  