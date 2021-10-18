from app.orm.repositories.base import BaseRepository
from app.orm.models import Unit


class UnitRepository(BaseRepository):
    __model__ = Unit
