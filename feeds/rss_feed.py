from sql_app.repositories.movie_repository import MovieRepo
from feedgenerator import RssFeed
from sqlalchemy.orm import Session


class LatestRssFeed(RssFeed):
    title: str
    price: float
    description: str

    @staticmethod
    def items(db: Session):
        return MovieRepo.fetch_all(db)

    @staticmethod
    def item_title(item):
        return item.title

    @staticmethod
    def item_price(item):
        return item.price

    @staticmethod
    def item_description(item):
        return item.description
