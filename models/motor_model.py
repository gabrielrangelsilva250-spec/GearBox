from sqlalchemy import Column, Float,Integer
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Motor(Base):
    id = Column(Integer,primary_key=True,index=True)
    Motor = Column(Integer)      #Em cm (ex: 2000, 1600)
    potencia_cv = Column(Integer)# Potência em cavalos
    potencia_kw = Column(Float)     #Potência em kW 
    torque_nm =Column(Integer)   #Torque em Nm
    velocidade_maxima = Column(Integer)  #Em km/h