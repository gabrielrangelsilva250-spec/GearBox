from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncSession
from core.configs import settings
from contextlib import asynccontextmanager

engine: AsyncEngine = create_async_engine(settings.DB_URL)

Session = sessionmaker(
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
    class_=AsyncSession,
    bind=engine
)

@asynccontextmanager
async def get_session() -> AsyncSession:
    async with Session() as session:
        yield session