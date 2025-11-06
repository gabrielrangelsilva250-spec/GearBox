from typing import List
from fastapi import APIRouter, Response, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import SessionLocal 
from models.car_models import Car
from schemas.car_schemas import CarCreate

async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CarCreate)
async def post_car(car: CarCreate, db: AsyncSession = Depends(get_db)):
    new_car = Car(
        Car_brand = car.Car_brand,
        model = car.model,
        motor_type = car.motor_type,
        release_year = car.release_year,
        Transmission_type = car.Transmission_type,
        car_license_plate= car.car_license_plate,
        Type_of_brake_system= car.Type_of_brake_system,
        price = car.price
    )
    db.add(new_car)
    await db.commit()
    await db.refresh(new_car)
    return new_car


@router.get("/", response_model=List[CarCreate])
async def get_all_cars(db: AsyncSession = Depends(get_db)):
    query = select(Car)
    result = await db.execute(query)
    cars = result.scalars().all()
    return cars


@router.get("/{car_id}", response_model=CarCreate)
async def get_car_by_id(car_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Car).filter(Car.id == car_id)
    result = await db.execute(query)
    car = result.scalar_one_or_none()
    
    if car:
        return car
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carro não encontrado")


@router.put("/{car_id}", response_model=CarCreate, status_code=status.HTTP_200_OK)
async def put_car(car_id: int, car_data: CarCreate, db: AsyncSession = Depends(get_db)):
    query = select(Car).filter(Car.id == car_id)
    result = await db.execute(query)
    car_up = result.scalar_one_or_none()
    
    if car_up:
        car_up.Car_brand = car_data.Car_brand
        car_up.model = car_data.model
        car_up.motor_type = car_data.motor_type
        car_up.release_year = car_data.release_year
        car_up.Transmission_type = car_data.Transmission_type
        car_up.car_license_plate = car_data.car_license_plate
        car_up.Type_of_brake_system = car_data.Type_of_brake_system
        car_up.price = car_data.price
        
        await db.commit()
        await db.refresh(car_up)
        return car_up
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carro não encontrado")


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_car(car_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Car).filter(Car.id == car_id)
    result = await db.execute(query)
    car_del = result.scalar_one_or_none() 
    
    if car_del:
        await db.delete(car_del)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carro não encontrado")