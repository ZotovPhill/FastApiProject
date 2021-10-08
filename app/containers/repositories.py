from dependency_injector import containers, providers

from app.core.settings import settings
from app.orm.repositories.base import Database
from app.orm.repositories.users.address_repository import AddressRepository
from app.orm.repositories.users.employee_repository import EmployeeRepository
from app.orm.schemas.base_schema import BaseIdModel


class DatabaseContainer(containers.DeclarativeContainer):
    db = providers.Singleton(Database, db_url=settings.database_url)
    serializer = providers.Singleton(BaseIdModel)
    employee_repository: EmployeeRepository = providers.Singleton(
        EmployeeRepository,
        session_factory=db.provided.session,
        serializer=serializer.provider
    )
    address_repository: AddressRepository = providers.Singleton(
        AddressRepository,
        session_factory=db.provided.session,
        serializer=serializer.provider
    )
