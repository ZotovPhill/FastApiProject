from app.orm.repositories.users.employee_repository import EmployeeRepository
from fastapi import APIRouter, Depends
from dependency_injector.wiring import inject, Provide
from app.containers.repositories import DatabaseContainer
from app.orm.schemas.query.users.employee_query import EmployeeQueryParam
from app.orm.schemas.response.users.employee_response import Employee
from app.orm.schemas.request.users.employee_request import Employee as EmployeeRequest
from app.services.security.auth_service import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_current_user)],
)


@router.get("")
@inject
def read_list(
        query: EmployeeQueryParam = Depends(EmployeeQueryParam.as_obj),
        employee_repository: EmployeeRepository = Depends(Provide[DatabaseContainer.employee_repository]),
):
    employee_repository.serializer = Employee
    return employee_repository.universal_filter_sort(query.filter, query.sort, query.paginator)


@router.post("")
@inject
def create(
        employee: EmployeeRequest,
        employee_repository: EmployeeRepository = Depends(Provide[DatabaseContainer.employee_repository])
):
    return employee_repository.create(employee)


@router.get("/{employee_id}")
@inject
def read(
        employee_id: int,
        employee_repository: EmployeeRepository = Depends(Provide[DatabaseContainer.employee_repository]),
):
    return employee_repository.find(employee_id)


@router.put("/{employee_id}")
@inject
def update(
        employee_id: int,
        employee: EmployeeRequest,
        employee_repository: EmployeeRepository = Depends(Provide[DatabaseContainer.employee_repository])
):
    employee.id = employee_id
    return employee_repository.update(employee)


@router.delete("/{employee_id}")
@inject
def delete(
        employee_id: int,
        employee_repository: EmployeeRepository = Depends(Provide[DatabaseContainer.employee_repository])
):
    employee_repository.delete(employee_id)
    return {}
