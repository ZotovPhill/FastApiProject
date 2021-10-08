from fastapi.applications import FastAPI
from app.containers.repositories import DatabaseContainer
from app.containers.security import SecurityContainer
from app.views.users import employee_view
from app.orm.fixtures.models.v1 import load_address
from app.services.security import auth_service
from app.commands import fixtures


def add_containers(app: FastAPI):
    database_container = DatabaseContainer()
    database_container.wire(modules=[
        employee_view,
        load_address,
        fixtures
    ])

    security_container = SecurityContainer()
    security_container.wire(modules=[
        auth_service
    ])

    app.container = [
        database_container,
        security_container,
    ]
