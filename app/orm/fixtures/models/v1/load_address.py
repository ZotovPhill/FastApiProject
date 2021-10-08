from dependency_injector.wiring import inject, Provide
from fpgen.orm.sqlalchemy.sqla_fixtures_loader import SQLAlchemyFixturesLoader

from app.containers.repositories import DatabaseContainer
from app.orm.repositories.users.address_repository import AddressRepository
from app.orm.schemas.request.users.address_request import Address


class LoadAddress(SQLAlchemyFixturesLoader):

    @inject
    def load(
            self,
            address_repository: AddressRepository = Provide[DatabaseContainer.address_repository]
    ) -> None:
        objects = [
            Address(
                street=self.fake.street_address(),
                city=self.fake.city(),
                state=self.fake.country(),
                zip=self.fake.postcode(),
            )
            for _ in range(self.quantity)
        ]
        address_repository.bulk_save(objects)

    @staticmethod
    def env_group() -> list:
        return ['dev', 'prod']
