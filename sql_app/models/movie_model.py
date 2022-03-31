from sqlalchemy import Column, Integer, String, Float
from sqlite_db.sqlite import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    title = Column(String(100), nullable=False, unique=False, index=True)
    subtitle = Column(String(150), nullable=True)
    price = Column(Float(precision=2), nullable=False)
    description = Column(String(200), nullable=True)

    # helper method to print the object at runtime
    def __repr__(self):
        return 'MovieModel(title=%s, subtitle=%s, price=%s, description=%s,)' \
               % (self.title, self.subtitle, self.price, self.description)