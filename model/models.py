import datetime
import os
from sqlalchemy import DateTime, Integer, String, func, Column, TIMESTAMP
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "q1w2e3r4t5y")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "flask")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")


engine = create_async_engine(
    f"postgresql+asyncpg://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
Session = async_sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase, AsyncAttrs):
    type_annotation_map = {
        datetime.datetime: TIMESTAMP(func.now())}


class Advertisement(Base):
    __tablename__ = "app_advertisements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(String(150), nullable=True)
    owner: Mapped[str] = mapped_column(String(72), nullable=False)
    registration_time: Mapped[datetime.datetime.now()] = mapped_column(DateTime, server_default=func.now())
