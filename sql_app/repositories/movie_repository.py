from sqlalchemy.orm import Session
from sql_app.models.movie_model import Movie
from sql_app.schemas.movie_schema import MovieCreate


class MovieRepo:

    @staticmethod
    async def create(db: Session, movie: MovieCreate):
        db_movie = Movie(
            title=movie.title,
            subtitle=movie.subtitle,
            price=movie.price,
            description=movie.description,
        )
        db.add(db_movie)
        db.commit()
        db.refresh(db_movie)
        return db_movie

    @staticmethod
    def fetch_movie_by_id(db: Session, _id):
        return db.query(Movie).filter(Movie.id == _id).first()

    @staticmethod
    def fetch_by_title(db: Session, title):
        return db.query(Movie).filter(Movie.title == title).first()

    @staticmethod
    def fetch_by_title_and_subtitle(db: Session, title, subtitle):
        return db.query(Movie).filter(Movie.title == title and Movie.subtitle == subtitle).first()

    @staticmethod
    def fetch_all(db: Session, skip: int = 0, limit: int = 50):
        return db.query(Movie).offset(skip).limit(limit).all()

    @staticmethod
    async def delete(db: Session, movie_id):
        db_movie = db.query(Movie).filter_by(id=movie_id).first()
        db.delete(db_movie)
        db.commit()

    @staticmethod
    async def update(db: Session, movie_data):
        updated_movie = db.merge(movie_data)
        db.commit()
        return updated_movie
