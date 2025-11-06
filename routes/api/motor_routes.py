from typing import List
from fastapi import APIRouter,Response, status, Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSessionLocal
from sqlalchemy.future import select
from core.database import SessionLocal
from models.motor_model import Motor
from schemas.motor_schemas import MotorCreate


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MotorCreate)
async def post_motor (motor: MotorCreate, db: AsyncSessionLocal= Depends(SessionLocal)):
    new_motor =Motor(
        Motor_motor = motor.Motor,
        potencia_cv_motor = motor.potencia_cv,
        potencia_kw_motor = motor.potencia_kw,
        torque_nm_motor = motor.torque_nm,
        velocidade_maxima_motor = motor.velocidade_maxima
    )
    db.add(new_motor)
    await db.commit()
    await db.refresh(new_motor)
    return new_motor

@router.get("/", response_model=List[MotorCreate])
async def get_motor(db: AsyncSessionLocal = Depends(SessionLocal)):
    async with db as SessionLocal:
        query = select(Motor)
        result = await SessionLocal.execute(query)
        Motor = result.scalars().all()
        return Motor
    
@router.get("/{motor_id}", response_model=MotorCreate)
async def get_motor(motor_id: int, db: AsyncSessionLocal = Depends(SessionLocal)):
    async with db as SessionLocal:
        query = select(Motor).filter(Motor.id == motor_id)
        result = await SessionLocal.execute(query)
        motor = result.scalar_one_or_none()
        if motor:
            return motor
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motor não encontrado")

@router.put("/{motor_id}", response_model=MotorCreate, status_code=status.HTTP_200_OK)
async def put_motor(motor_id: int, motor_data: MotorCreate, db: AsyncSessionLocal = Depends(SessionLocal)):
    async with db as SessionLocal:
        query = select(Motor).filter(Motor.id == motor_id)
        result = await SessionLocal.execute(query)
        motor_up = result.scalar_one_or_none()

        if motor_up:
            motor_up.Motor = motor_data.Motor,
            motor_up.potencia_cv = motor_data.potencia_cv
            motor_up.potencia_kw
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motor não encontrado")            


@router.delete("/{motor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_motor(motor_id: int, db: AsyncSessionLocal = Depends(SessionLocal)):
    async with db as SessionLocal:
        query = select(Motor).filter(Motor.id == motor_id)
        result = await SessionLocal.execute(query)
        motor_del = result.scalar_one_or_none()

        if motor_del:
            await SessionLocal.delete(motor_del)
            await SessionLocal.commit()
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motor não encontrado")