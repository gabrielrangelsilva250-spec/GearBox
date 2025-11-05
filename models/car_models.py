from datetime import datetime
from sqlalchemy import TIMESTAMP, Column,Integer,String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Car(Base):
    id = Column(Integer,primary_key=True,index=True)
    Car_brand = Column(String(30))
    model=  Column(String(30))
    motor_type = Column(String(30))
    release_year = Column(TIMESTAMP, default=datetime.utcnow)
    Transmission_type = Column(String(30))
    car_license_plate = Column(String(30))
    Type_of_brake_system =Column(String(30)) 
    price = Column(Integer)
