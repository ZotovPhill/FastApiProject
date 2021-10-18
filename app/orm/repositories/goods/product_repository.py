from app.orm.repositories.base import BaseRepository
from app.orm.models import Product


class ProductRepository(BaseRepository):
    __model__ = Product
