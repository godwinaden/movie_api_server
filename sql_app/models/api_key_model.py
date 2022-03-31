from sqlalchemy import Column, Integer, String
from sqlalchemy_utils import StringEncryptedType

from sqlite_db.sqlite import Base

encryption_key = "Switz123R5"


class ApiKey(Base):
    __tablename__ = 'api_keys'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    secret = Column(StringEncryptedType(String, key=encryption_key), nullable=False, unique=True)
    public = Column(StringEncryptedType(String, key=encryption_key), nullable=False, unique=True)
    domain = Column(String(100), nullable=False, unique=True)

    # helper method to print the object at runtime
    def __repr__(self):
        return 'ApiKeyModel(secret=%s, public=%s, domain=%s)' \
               % (self.secret, self.public, self.domain)
