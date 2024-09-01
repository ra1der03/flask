import datetime
import os
from atexit import register

from sqlalchemy import DateTime, Integer, String, create_engine, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "q1w2e3r4t5y")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "flask")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")


engine = create_engine(
    f"postgresql://"
    f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


class Advertisement(Base):
    __tablename__ = "app_advertisements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(64), nullable=False)
    description: Mapped[str] = mapped_column(String(150), nullable=False)
    owner: Mapped[str] = mapped_column(String(72), nullable=False)
    registration_time: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )

    @property
    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "owner": self.owner,
            "registration_time": self.registration_time.isoformat(),
        }


Base.metadata.create_all(bind=engine)
register(engine.dispose)
