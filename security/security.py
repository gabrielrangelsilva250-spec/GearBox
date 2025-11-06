from passlib.context import CryptContext
from jose import JWTError,jwt
from datetime import datetime,timedelta
import os

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Configurações JWT
SECRET_KEY = os.getenv("SECRET_KEY","sua-chave-secreta-aqui")
ALGORITIHM = "HS256"
ACESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password:str, hashed_password: str) -> bool:
    """Verfica se uma senha em texto puro a um hash
    
    Args:
    plain_password: A senha que o usuário digitou(em texto puro).
    hashed_password: O hash de senha armazenado no banco de dados

    Returns:
    True se as senhas coincidirem, False caso contrário
    """
   
    return pwd_context.verify(plain_password,hashed_password)

def get_password_hash(password: str) -> str:
    """Gera hash bcrypt da senha"""
    return pwd_context.hash(password)

def create_acess_token(data: dict,expires_delta: timedelta = None):
    """Cria Token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp":expire})

def verify_token(token: str):
    """Verifica e decodifica token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITIHM])
        return payload
    except JWTError:
        return None