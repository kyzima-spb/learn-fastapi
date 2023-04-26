from __future__ import annotations
import typing as t

import sqlalchemy as sa
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from .database import Base
from .fastapi_bcrypt import Bcrypt


bcrypt = Bcrypt()

int_pk = t.Annotated[int, mapped_column(primary_key=True, sort_order=-1)]
role_fk = t.Annotated[int, mapped_column(
    sa.ForeignKey('role.id', onupdate='CASCADE', ondelete='RESTRICT'),
)]


class User(Base):
    __tablename__ = 'user'

    id: Mapped[int_pk]
    email: Mapped[str] = mapped_column(sa.String(50), unique=True)
    _password: Mapped[str] = mapped_column('password', sa.String(100))
    # role_id: Mapped[role_fk]
    firstname: Mapped[str] = mapped_column(sa.String(255))
    lastname: Mapped[str] = mapped_column(sa.String(255))
    is_active: Mapped[bool]
    allow_personal_data: Mapped[bool]

    def change_password(self, value: str) -> None:
        """Changes the current password to passed."""
        self._password = bcrypt.generate_password_hash(value).decode('utf-8')

    def check_password(self, password: str) -> bool:
        """Returns true if the password is valid, false otherwise."""
        return bcrypt.check_password_hash(self._password, password)

    password = property(fset=change_password)

    @classmethod
    def find_by_username(cls, session: sa.orm.Session, email: str) -> t.Optional[User]:
        """Returns the user with passed email, or None."""
        stmt = sa.select(cls).where(cls.email == email)
        return session.scalars(stmt).first()


class Role(Base):
    __tablename__ = 'role'

    id: Mapped[int_pk]
    name: Mapped[str] = mapped_column(sa.String(30), unique=True)
    description: Mapped[t.Optional[str]] = mapped_column(sa.String(500), default='')


class Genre(Base):
    __tablename__ = 'genre'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(30))


class Game(Base):
    __tablename__ = 'game'

    id: Mapped[int] = mapped_column(primary_key=True)
    genre_id: Mapped[int] = mapped_column(sa.ForeignKey('genre.id'))
    genre: Mapped[t.List[Genre]] = relationship(backref='games')
    title: Mapped[str] = mapped_column(sa.String(500))
    cost: Mapped[float]
    description: Mapped[str] = mapped_column(sa.Text, default='')
