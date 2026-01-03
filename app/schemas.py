from typing import Optional, Annotated
from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    title: Annotated[str, Field(max_length=255)]
    author: Annotated[str, Field(max_length=255)]
    genre: Annotated[str, Field(max_length=64)]
    year: Annotated[int, Field(ge=0, le=2100)]
    rating: Annotated[float, Field(ge=0.0, le=5.0)]


class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    genre: str
    year: int
    rating: float


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    genre: Optional[str] = None
    year: Optional[int] = None
    rating: Optional[float] = None