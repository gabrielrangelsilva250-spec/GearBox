from sqlalchemy import Column,Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Transmission_type(Base):
    id = Column(Integer, primary_key=True, index=True)
    Transmission =Column(String(20))
    num_marches = Column(Integer)
    traction = Column(String(10))  