from typing import List
from fastapi import APIRouter, Response, status, Depends, HTTPException 
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy.future import select
from core.database import SessionLocal
from models.user_models import User
from schemas.user_schemas import UserCreate, UserLogin, UserResponse

async def get_db() -> AsyncSession:
    async with SessionLocal() as db:
        yield db

router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def post_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(User).filter(User.username == user.username)
    result = await db.execute(query)
    existing_user = result.scalar_one_or_none()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username já existe"
        )
    
    new_user = User(
        username = user.username,
        hashed_password = "default_password" 
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/", response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    query = select(User)
    result = await db.execute(query)
    users = result.scalars().all() 
    return users

@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(user_id: int, db: AsyncSession = Depends(get_db)):
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    
    if user:
        return user
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def put_user(user_id: int, user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user_up = result.scalar_one_or_none()

    if user_up:
        if user_data.username != user_up.username:
            check_query = select(User).filter(User.username == user_data.username, User.id != user_id)
            check_result = await db.execute(check_query)
            existing_user = check_result.scalar_one_or_none()
            
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username já está em uso"
                )
        
        user_up.username = user_data.username
        await db.commit() 
        await db.refresh(user_up) 
        return user_up
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    query = select(User).filter(User.id == user_id)
    result = await db.execute(query)
    user_del = result.scalar_one_or_none()

    if user_del:
        await db.delete(user_del)
        await db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuário não encontrado")