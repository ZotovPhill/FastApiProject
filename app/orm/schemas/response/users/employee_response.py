from pydantic.main import BaseModel
from app.orm.schemas.base_schema import BaseIdModel


class Employee(BaseIdModel):
    email: str


class EmployeesList(BaseModel):
    employees: list[Employee] = []

    class Config:
        orm_mode = True
