from app.orm.repositories.base import BaseRepository
from app.orm.models import Address


class AddressRepository(BaseRepository):
    __model__ = Address
