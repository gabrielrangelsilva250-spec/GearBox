from datetime import datetime
from pydantic import BaseModel

class CarCreate(BaseModel):
    Car_brand: str
    model: str
    motor_type: str
    release_year: datetime
    Transmission_type: str
    car_license_plate: str
    Type_of_brake_system :str
    price: int