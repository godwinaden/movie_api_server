from typing import Optional
from pydantic import BaseModel


class ApiKeyBase(BaseModel):
    secret: Optional[str] = None
    public: Optional[str] = None
    domain: str


class ApiKeyCreate(ApiKeyBase):
    pass


class ApiKey(ApiKeyBase):
    id: int

    class Config:
        orm_mode = True


class ApiDomain(ApiKeyBase):
    domain: str

    class Config:
        orm_mode = True


class ApiKeyUpdate(ApiKeyBase):
    id: int
