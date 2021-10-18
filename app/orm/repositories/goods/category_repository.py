from app.orm.repositories.base import BaseRepository
from app.orm.models import Category


class CategoryRepository(BaseRepository):
    __model__ = Category
