import base64
import os
import random
import string
from sqlalchemy.orm import Session
from sql_app.models.api_key_model import ApiKey
from sql_app.schemas.api_key_schema import ApiKeyCreate


class ApiKeyRepo:

    @staticmethod
    async def create(db: Session, api_key: ApiKeyCreate):
        db_api_key = ApiKey(
            secret=api_key.secret,
            public=api_key.public,
            domain=api_key.domain,
        )
        db.add(db_api_key)
        db.commit()
        db.refresh(db_api_key)
        return db_api_key

    @staticmethod
    def fetch_api_key_by_id(db: Session, _id):
        return db.query(ApiKey).filter(ApiKey.id == _id).first()

    @staticmethod
    def fetch_by_secret(db: Session, secret):
        return db.query(ApiKey).filter(ApiKey.secret == secret).first()

    @staticmethod
    def fetch_by_public(db: Session, public):
        return db.query(ApiKey).filter(ApiKey.public == public).first()

    @staticmethod
    def fetch_by_domain(db: Session, domain):
        return db.query(ApiKey).filter(ApiKey.domain == domain).first()

    @staticmethod
    def fetch_by_public_domain(db: Session, public, domain):
        return db.query(ApiKey).filter(ApiKey.public == public and ApiKey.domain == domain).first()

    @staticmethod
    async def delete(db: Session, api_key_id):
        db_api_key = db.query(ApiKey).filter_by(id=api_key_id).first()
        db.delete(db_api_key)
        db.commit()

    @staticmethod
    async def update(db: Session, api_key_data):
        updated_api_key = db.merge(api_key_data)
        db.commit()
        return updated_api_key

    @staticmethod
    def generate_public_key(length: int = 50) -> str:
        choices = string.ascii_letters + string.digits
        alt_chars = ''.join([choices[ord(os.urandom(1)) % 62] for _ in range(2)]).encode("utf-8")
        api_key = base64.b64encode(os.urandom(length), altchars=alt_chars).decode("utf-8")
        return api_key

    @staticmethod
    def generate_secret_key(length: int = 50) -> str:
        key = ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(length))
        return key
