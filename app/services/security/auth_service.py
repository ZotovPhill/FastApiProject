from datetime import timedelta, datetime

from dependency_injector.wiring import Provide
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext

from app.containers.security import SecurityContainer
from app.core.settings import settings
from app.exceptions.exceptions import AuthenticationException, AccessDeniedException
from app.orm.models import Employee
from app.orm.repositories.users.employee_repository import EmployeeRepository

pwd_context: CryptContext = Provide[SecurityContainer.pwd_context]
employee_repository: EmployeeRepository = Provide[SecurityContainer.database.employee_repository]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def authenticate_user(
        username: str,
        password: str,
) -> Employee:
    employee = employee_repository.find_by_email(username)
    if not employee:
        raise AuthenticationException(detail="Could not validate username")
    if not verify_password(password, employee.password):
        raise AuthenticationException(detail="Could not validate password")
    return employee


def create_access_token(data: dict) -> tuple[str, str]:
    encoded_jwt = jwt.encode(
        _token_payload(data, settings.access_token_expires),
        settings.secret_key,
        algorithm=settings.algorithm
    )
    refresh_token = jwt.encode(
        _token_payload(data, settings.refresh_token_expires),
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt, refresh_token


def _token_payload(data: dict, expires_time: int = 30):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(seconds=expires_time)
    to_encode.update({"exp": expire})

    return to_encode


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Employee:
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=settings.algorithm)
        username: str = payload.get("sub")
        if username is None:
            raise AccessDeniedException
    except JWTError:
        raise AccessDeniedException
    employee = employee_repository.find_by_email(username)
    if not employee or not employee.is_active:
        raise AccessDeniedException

    return employee
