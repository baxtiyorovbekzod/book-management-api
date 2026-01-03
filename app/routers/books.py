from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookUpdate, BookResponse

router = APIRouter(
    prefix="/books",
    tags=["Books"],
)

@router.get("/", response_model=list[BookResponse])
def get_all_books(
    db: Annotated[Session, Depends(get_db)]
):
    return db.query(Book).all()

@router.get("/{book_id}", response_model=BookResponse)
def get_one_book(
    book_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )
    return book

@router.post(
    "/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED
)
def create_book(
    book: BookCreate,
    db: Annotated[Session, Depends(get_db)]
):
    new_book = Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

@router.put("/{book_id}", response_model=BookResponse)
def update_book(
    book_id: int,
    book: BookUpdate,
    db: Annotated[Session, Depends(get_db)]
):
    existing_book = db.query(Book).filter(Book.id == book_id).first()
    if not existing_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    for key, value in book.model_dump(exclude_unset=True).items():
        setattr(existing_book, key, value)

    db.commit()
    db.refresh(existing_book)
    return existing_book

@router.delete(
    "/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_book(
    book_id: int,
    db: Annotated[Session, Depends(get_db)]
):
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Book not found"
        )

    db.delete(book)
    db.commit()

@router.get("/search", response_model=list[BookResponse])
def search_books(
    search: str,
    db: Annotated[Session, Depends(get_db)]
):
    return (
        db.query(Book)
        .filter(
            Book.title.ilike(f"%{search}%") |
            Book.author.ilike(f"%{search}%")
        )
        .all()
    )

