from typing import List, Optional
from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    price: float
    description: Optional[str] = None


class MovieCreate(MovieBase):
    pass


class Movie(MovieBase):
    id: int

    class Config:
        orm_mode = True


class Movies(MovieBase):
    id: int
    movies: List[Movie]

    class Config:
        orm_mode = True


class MovieUpdate(MovieBase):
    id: int
