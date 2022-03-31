from feedgenerator import Atom1Feed
from sqlalchemy.orm import Session

from sql_app.repositories.movie_repository import MovieRepo


class LatestAtomFeed(Atom1Feed):
    title: str
    price: float
    feed_type = Atom1Feed
    subtitle: str

    @staticmethod
    def items(db: Session):
        return MovieRepo.fetch_all(db)

    @staticmethod
    def item_title(item):
        return item.title

    @staticmethod
    def item_subtitle(item):
        return item.subtitle

    @staticmethod
    def item_price(item):
        return item.price
