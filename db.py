from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
import logging
import os
from models.db_models import Base, Route


DATABASE_URL = os.getenv('DATABASE_URL')

logger = logging.getLogger(__name__)

engine = create_async_engine(DATABASE_URL)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()


async def get_db():
    async with Session() as session:
        yield session

    
async def new_route(item: Route, db: AsyncSession = Depends(get_db)):
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

async def get_route_by_id(id: int, db: AsyncSession = Depends(get_db)):
    route = await db.get(Route, id)
    return route
