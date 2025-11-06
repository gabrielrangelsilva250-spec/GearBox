from typing import List
from fastapi import APIRouter,Response, status, Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from core.database import SessionLocal
from models.transmission_type_models import Transmission_type
from schemas.transmission_schemas import TransmissionCreate

async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=TransmissionCreate)
async def post_transmission (transmission: TransmissionCreate, db: AsyncSession = Depends(get_db)):
    new_transmission = Transmission_type(
        Transmission_transmission = transmission.Transmission,
        num_marche_transmission = transmission.num_marche, 
        traction = transmission.traction
    )
    db.add(new_transmission)
    await db.commit()
    await db.refresh(new_transmission)
    return new_transmission



@router.get("/", response_model=List[TransmissionCreate])
async def get_all_transmissions(db: AsyncSession = Depends(get_db)):
    query = select(Transmission_type)
    result = await db.execute(query)
    transmissions = result.scalars().all() 
    return transmissions


@router.get("/{transmission_id}", response_model=TransmissionCreate)
async def get_transmission_by_id(transmission_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Transmission_type).filter(Transmission_type.id == transmission_id)
    result = await db.execute(query)
    transmission = result.scalar_one_or_none()
    
    if transmission:
        return transmission
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transmissão não encontrada")
    


@router.put("/{transmission_id}", response_model=TransmissionCreate, status_code=status.HTTP_200_OK)
async def put_transmission(transmission_id: int, transmission_data: TransmissionCreate, db: AsyncSession = Depends(get_db)):
    query = select(Transmission_type).filter(Transmission_type.id == transmission_id)
    result = await db.execute(query)
    transmission_up = result.scalar_one_or_none()

    if transmission_up:
 
        transmission_up.Transmission_transmission = transmission_data.Transmission
        transmission_up.num_marche_transmission = transmission_data.num_marche
        transmission_up.traction = transmission_data.traction 
        
        await db.commit() 
        await db.refresh(transmission_up) 
        return transmission_up
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transmissão não encontrada")  


@router.delete("/{transmission_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transmission(transmission_id: int, db: AsyncSession = Depends(get_db)):
    query = select(Transmission_type).filter(Transmission_type.id == transmission_id)
    result = await db.execute(query)
    transmission_del = result.scalar_one_or_none()

    if transmission_del:
        await db.delete(transmission_del)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transmissão não encontrada")    