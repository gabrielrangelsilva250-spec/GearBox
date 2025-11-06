from typing import List
from fastapi import APIRouter, Response, status, Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import SessionLocal 
from models.motor_model import Motor
from schemas.motor_schemas import MotorCreate

async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=MotorCreate)
async def post_motor (motor: MotorCreate, db: AsyncSession = Depends(get_db)):
    new_motor = Motor(
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
async def get_all_motors(db: AsyncSession = Depends(get_db)):
    query = select(Motor)
    result = await db.execute(query)
    motors = result.scalars().all() 
    return motors
    


@router.get("/{motor_id}", response_model=MotorCreate)
async def get_motor_by_id(motor_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Motor).filter(Motor.id == motor_id)
    result = await db.execute(query)
    motor = result.scalar_one_or_none()
    
    if motor:
        return motor
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motor não encontrado")



@router.put("/{motor_id}", response_model=MotorCreate, status_code=status.HTTP_200_OK)
async def put_motor(motor_id: int, motor_data: MotorCreate, db: AsyncSession = Depends(get_db)):

    query = select(Motor).filter(Motor.id == motor_id)
    result = await db.execute(query)
    motor_up = result.scalar_one_or_none()

    if motor_up:

        motor_up.Motor_motor = motor_data.Motor
        motor_up.potencia_cv_motor = motor_data.potencia_cv
        motor_up.potencia_kw_motor = motor_data.potencia_kw 
        motor_up.torque_nm_motor = motor_data.torque_nm
        motor_up.velocidade_maxima_motor = motor_data.velocidade_maxima

        await db.commit()
        await db.refresh(motor_up) 
        return motor_up
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motor não encontrado")



@router.delete("/{motor_id}", status_code=status.HTTP_204_NO_CONTENT)

async def delete_motor(motor_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Motor).filter(Motor.id == motor_id)
    result = await db.execute(query)
    motor_del = result.scalar_one_or_none()

    if motor_del:
        await db.delete(motor_del)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motor não encontrado")