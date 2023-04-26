from __future__ import annotations
import typing as t

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Genre
from ..schemas.genres import GenreCreateSchema, GenreSchema


router = APIRouter(
    prefix='/genres',
    tags=['Genres'],
)


@router.get(
    '/',
    response_model=t.List[GenreSchema],
    summary='Get all game genres',
)
async def index(db: t.Annotated[Session, Depends(get_db)]):
    """Returns all elements of the collection of game genres."""
    stmt = select(Genre)
    return db.scalars(stmt).all()


@router.post(
    '/',
    response_model=GenreSchema,
    status_code=201,
    summary='Add a game genre'
)
def create(
    payload: GenreCreateSchema,
    db: t.Annotated[Session, Depends(get_db)]
):
    genre = Genre(**payload.dict())
    db.add(genre)
    db.commit()
    # db.refresh(genre)
    return genre
