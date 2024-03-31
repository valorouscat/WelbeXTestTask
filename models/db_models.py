from sqlalchemy import Column, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Route(Base):
    __tablename__ = 'Routes'

    id = Column(Integer, primary_key=True)
    points = Column(JSONB)

    