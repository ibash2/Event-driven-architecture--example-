from typing import AsyncGenerator

from sqlalchemy import (
    Column,
    CursorResult,
    Insert,
    Integer,
    Select,
    String,
    Update,
)
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

DATABASE_URL = str(settings.DATABASE_URL)

async_engine = create_async_engine(DATABASE_URL)
Base_a = declarative_base()


class Base(Base_a):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


metadata = Base.metadata


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, index=True)
    quantity = Column(Integer)


# Асинхронные запросы в базу
async def fetch_one(select_query: Select | Insert | Update):
    async with async_engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return cursor.first() if cursor.rowcount > 0 else None


async def fetch_all(select_query: Select | Insert | Update) -> list:
    async with async_engine.begin() as conn:
        cursor: CursorResult = await conn.execute(select_query)
        return [r for r in cursor.all()]


async def execute(select_query: Insert | Update) -> None:
    async with async_engine.begin() as conn:
        return await conn.execute(select_query)


engine = create_async_engine(settings.DATABASE_URL, echo=True)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession
)


async def get_db() -> AsyncGenerator[SessionLocal, None]:
    async with SessionLocal() as session:
        yield session
