"""This module contains the enroll routes."""
from typing import Annotated
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from src.models.schemas import Enrollments
from src.database.database import get_db
from src.schemas.schemas import PinModel, ResponseModel
from .employees import get_employee_by_id

_enroll = APIRouter()

@_enroll.post("/{employee_id}/pin", response_model=ResponseModel[PinModel])
async def create_pin(
    data: PinModel,
    employee_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    db: Session=Depends(get_db)
):
    """Create a new pin for an employee."""
    employee = await get_employee_by_id(employee_id, db)

    if not employee.enrollments:
        enroll = Enrollments(employee_id=employee.id, pin=data.pin)
    else:
        enroll = employee.enrollments
        enroll.pin = data.pin

    db.add(enroll)
    db.commit()
    return {"data": enroll}