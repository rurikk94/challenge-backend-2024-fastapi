import sys
from typing import Annotated, List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from src.models.schemas import Employee
from src.database.database import get_db
from src.repository.repository import get_all, get_by_id, create
from src.schemas.schemas import EmployeeDBModel, ResponseModel, EmployeeDataModel


_employees = APIRouter()


@_employees.get("/", tags=["employees"], response_model=ResponseModel[EmployeeDBModel])
async def employees(db: Session = Depends(get_db)):
    """Get all employees."""
    empleados = get_all(db, Employee)
    return {"data": empleados}

@_employees.get("/{employee_id}", tags=["employees"], response_model=ResponseModel[EmployeeDBModel])
async def employee_by_id(
    employee_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    db: Session = Depends(get_db)
):
    """Get an employee by ID."""
    employee = await get_employee_by_id(employee_id, db)
    return {"data": employee}


async def get_employee_by_id(employee_id, db) -> Employee:
    """Get an employee by ID."""
    return get_by_id(db, Employee, employee_id)

async def get_employee_by_dni(dni, db) -> Employee:
    """Get an employee by DNI."""
    return db.query(Employee).filter(Employee.dni == dni).first()

@_employees.post("/", tags=["employees"], response_model=ResponseModel[EmployeeDBModel])
async def employee_create(employee: EmployeeDataModel, db: Session = Depends(get_db)):
    """Create a new employee."""

    new_employee = Employee(**employee.model_dump())
    db.add(new_employee)
    db.commit()
    return {"data": new_employee}

@_employees.put("/{employee_id}", tags=["employees"], response_model=ResponseModel[EmployeeDBModel])
async def employee_update(
    employee_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    employee_data: EmployeeDataModel,
    db: Session = Depends(get_db)
):
    """Update an employee."""
    employee: Employee = get_by_id(db, Employee, employee_id)
    employee.update_from_dict(employee_data.model_dump())
    db.commit()
    return {"data": employee}

@_employees.delete("/{employee_id}", tags=["employees"], response_model=ResponseModel[EmployeeDBModel])
async def employee_delete(
    employee_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    db: Session = Depends(get_db)
):
    """Delete an employee."""
    employee: Employee = get_by_id(db, Employee, employee_id)
    db.delete(employee)
    db.commit()
    return {"data": employee}