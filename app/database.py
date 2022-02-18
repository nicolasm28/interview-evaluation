from sqlalchemy import create_engine, Column, Integer, String, Boolean, null
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from .core.config import settings

engine = create_engine(settings.DATABASE_URI, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

Base = declarative_base()

# generating models
Base.metadata.create_all(bind=engine)