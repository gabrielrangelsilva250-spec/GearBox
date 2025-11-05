from types import Generator
from sqlalchemy.ext.associationproxy import AsyncSession
from core.database import Session

async def get_session() -> Generator:
    session: AsyncSession = Session()
    try:
        yield session
    finally:
        await session.close ()    