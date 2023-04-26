from __future__ import annotations
from datetime import datetime, timedelta
import typing as t

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)
from fastapi import status
from fastapi.security import (
    OAuth2PasswordBearer,
    OAuth2PasswordRequestFormStrict,
)
from jose import jwt, JWTError
from pydantic import BaseSettings
from sqlalchemy.orm import Session

from .database import get_db
from .models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


class OAuth2Config(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = 'HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30


class Auth:
    def __init__(self, config: OAuth2Config) -> None:
        self.config = config

    def authenticate_user(
        self,
        session: Session,
        username: str,
        password: str,
    ) -> t.Optional[User]:
        user = User.find_by_username(session, username)
        if user is not None and user.check_password(password):
            return user
        return None

    def create_access_token(self, payload: t.Dict[str, t.Any]) -> str:
        expires_at = datetime.utcnow() + timedelta(minutes=self.config.ACCESS_TOKEN_EXPIRE_MINUTES)
        return jwt.encode(
            claims={
                'exp': expires_at,
                'iat': datetime.utcnow(),
                **payload,
            },
            key=self.config.SECRET_KEY,
            algorithm=self.config.ALGORITHM,
        )

    def decode_access_token(self, token: str) -> t.Optional[t.Dict[str, t.Any]]:
        try:
            return jwt.decode(
                token=token,
                key=self.config.SECRET_KEY,
                algorithms=[self.config.ALGORITHM]
            )
        except JWTError:
            return None


def get_auth() -> Auth:
    return Auth(OAuth2Config())


def get_current_user(
    auth: t.Annotated[Auth, Depends(get_auth)],
    token: t.Annotated[str, Depends(oauth2_scheme)],
    session: t.Annotated[Session, Depends(get_db)],
) -> User:
    payload = auth.decode_access_token(token)

    if payload and 'sub' in payload:
        username = payload['sub']
        user = User.find_by_username(session, username)

        if user is not None:
            return user

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )


def get_current_active_user(
    current_user: t.Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail='Inactive user')
    return current_user


router = APIRouter(
    prefix='/auth',
    tags=['OAuth2'],
)


@router.post('/token')
def token(
    auth: t.Annotated[Auth, Depends(get_auth)],
    form: t.Annotated[OAuth2PasswordRequestFormStrict, Depends()],
    session: t.Annotated[Session, Depends(get_db)],
):
    user = auth.authenticate_user(session, form.username, form.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Incorrect username or password',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return {
        'access_token': auth.create_access_token({'sub': user.email}),
        'token_type': 'bearer',
    }


@router.get('/profile')
def profile(
    user: t.Annotated[User, Depends(get_current_active_user)],
):
    return f'{user.firstname} {user.lastname}'
