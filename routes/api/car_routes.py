from typing import List
from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSessionLocal
from sqlalchemy.future import select
from core.database import SessionLocal
from models.car_models import Car
from schemas.car_schemas import CarCreate

router = APIRouter()

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=CarCreate)
async def post_car(car: CarCreate, db:AsyncSessionLocal = Depends(SessionLocal)):
    new_car = Car(
        Car_brand = car.Car_brand_,
        model = car.model,
        motor_type = car.motor_type
        release_year
        Transmission_type
        car_license_plate
        Type_of_brake_system
        price
    )