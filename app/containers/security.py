from dependency_injector import containers, providers
from passlib.context import CryptContext

from app.containers.repositories import DatabaseContainer


class SecurityContainer(containers.DeclarativeContainer):
    pwd_context: CryptContext = providers.Singleton(CryptContext, schemes=["bcrypt"], deprecated="auto")
    database = providers.Container(DatabaseContainer)
