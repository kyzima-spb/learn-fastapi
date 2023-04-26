from __future__ import annotations
import asyncio
import typing as t

from fastapi import APIRouter, Depends, HTTPException
from fastapi import status
from sqlalchemy import select, text
from sqlalchemy.exc import IntegrityError

from ..database import get_db, SessionLocal
from ..models import User
from ..schemas.users import UserSchema, UserCreateSchema


router = APIRouter(
    prefix='/users',
    tags=['Users'],
)


@router.get('/test')
async def index(session: t.Annotated[SessionLocal, Depends(get_db)],):
    _ = await session.execute(text('select 1'))
    await asyncio.sleep(1)
    return {'hello': 'world'}


@router.get(
    '/',
    response_model=t.List[UserSchema],
    summary='Get all users',
)
async def index(
    session: t.Annotated[SessionLocal, Depends(get_db)],
):
    """Returns all elements of the collection users."""
    stmt = select(User)
    result = await session.scalars(stmt)
    return result.all()


@router.post(
    '/',
    response_model=UserSchema,
    status_code=201,
    summary='Create a new user',
)
async def create(
    payload: UserCreateSchema,
    session: t.Annotated[SessionLocal, Depends(get_db)],
):
    user = User(is_active=False, **payload.dict())
    session.add(user)

    try:
        session.commit()
        return user
    except IntegrityError as err:
        _, msg = err.orig.args

        if msg.startswith('Duplicate entry'):
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f'Пользователь с email-адресом {user.email!r} уже существует.'
            )

        raise err
