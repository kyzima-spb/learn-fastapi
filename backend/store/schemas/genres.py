from pydantic import BaseModel


class GenreBaseSchema(BaseModel):
    name: str


class GenreCreateSchema(GenreBaseSchema):
    pass


class GenreSchema(GenreBaseSchema):
    id: int

    class Config:
        orm_mode = True
