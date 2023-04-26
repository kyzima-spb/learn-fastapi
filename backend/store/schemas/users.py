from __future__ import annotations
import typing as t

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    validator,
    constr,
    SecretStr,
    ConstrainedStr,
    AnyHttpUrl,
    AnyUrl,
    stricturl,
)
from pydantic.errors import AnyStrMaxLengthError


class UserBaseSchema(BaseModel):
    email: EmailStr
    firstname: constr(min_length=1, max_length=255)
    lastname: constr(min_length=1, max_length=255)

    @validator('email')
    def validate_email_length(cls, value):
        max_length = 50
        if len(value) > max_length:
            raise AnyStrMaxLengthError(limit_value=max_length)
        return value


class UserCreateSchema(UserBaseSchema):
    password: str
    allow_personal_data: bool

    @validator('allow_personal_data')
    def validate_allow_personal_data(cls, value):
        if not value:
            raise ValueError(
                'Если вы отказываетесь от передачи и хранения личных данных,'
                ' то дальнейшие действия не возможны.'
            )
        return value


class UserSchema(UserBaseSchema):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
