from app.containers.repositories import DatabaseContainer
from app.orm.fixtures.models.v1 import load_address

database_container = DatabaseContainer()

database_container.wire(modules=[load_address])
