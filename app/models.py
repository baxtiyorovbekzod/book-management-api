from sqlalchemy import (
    Column,
    Integer,
    String,
    Float, 
)

from .database import Base


class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(length=255), nullable=False)
    author = Column(String(length=255), nullable=False)
    genre = Column(String(length=100), nullable=False)
    year = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)

    def __str__(self):
        return self.title