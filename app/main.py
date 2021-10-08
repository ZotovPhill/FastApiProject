from app.containers.base import add_containers
from app.services.logging.intercept_handler import CustomizeLogger
from fastapi import FastAPI
from app.exceptions.handlers import add_exception_handlers
from app.views.router import api_router


def create_app():
    app = FastAPI()
    app.include_router(api_router)
    add_containers(app)
    add_exception_handlers(app)
    app.logger = CustomizeLogger.make_logger()

    return app


app = create_app()
