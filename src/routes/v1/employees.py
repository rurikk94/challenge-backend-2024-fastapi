import sys
from typing import Annotated, List
from fastapi import APIRouter, Depends, Path

from src.models.schemas import Employee
from src.database.database import get_db
from src.repository.repository import get_all, get_by_id
from src.schemas.schemas import EmployeeDBModel, ResponseModel


_employees = APIRouter()


@_employees.get("/", tags=["employees"], response_model=ResponseModel[EmployeeDBModel])
async def employees(db = Depends(get_db)):
    empleados = get_all(db, Employee)
    return {"data": empleados}

@_employees.get("/{employee_id}", tags=["employees"], response_model=ResponseModel[EmployeeDBModel])
async def employee_by_id(
    employee_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    db = Depends(get_db)
):
    return await get_employee_by_id(employee_id, db)


async def get_employee_by_id(employee_id, db):
    employee: EmployeeDBModel = get_by_id(db, Employee, employee_id)
    return {"data": employee}