from pydantic.class_validators import validator

from app.orm.schemas.base_schema import BaseIdModel

from app.services.security.auth_service import get_password_hash


class Employee(BaseIdModel):
    email: str
    password: str

    @validator('password')
    def hash_password(cls, pw: str) -> str:
        return get_password_hash(pw)
