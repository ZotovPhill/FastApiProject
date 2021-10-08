from typing import Optional

from fastapi import HTTPException
from starlette import status


class NotFoundException(Exception):
    entity_name: str = "Entity"

    def __init__(self, entity_id, entity_name: Optional[str] = None):
        super().__init__(f'{entity_name or self.entity_name} not found, id: {entity_id}')


class UserNotFoundException(NotFoundException):
    entity_name: str = 'User'


class AuthenticationException(HTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = "Could not validate credentials"
    headers = {"WWW-Authenticate": "Bearer"}

    def __init__(self, detail: Optional[str] = None, headers: Optional[str] = None):
        super().__init__(self.status_code, detail or self.detail, headers or self.headers)


class AccessDeniedException(AuthenticationException):
    status_code = status.HTTP_403_FORBIDDEN
    detail = "Access Denied"
    headers = {"WWW-Authenticate": "Bearer"}
