"""This module contains the enroll routes."""
from datetime import datetime, UTC
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.models.schemas import Punch, PunchTypeEnum
from src.database.database import get_db
from src.schemas.schemas import PunchPinModel, ResponseModel, PunchDBModel
from .employees import get_employee_by_dni
from .devices import get_device_by_id
from src.exceptions import NotFoundException

_punch = APIRouter()

@_punch.post("/pin", response_model=ResponseModel[PunchDBModel])
async def create_punch(
    data: PunchPinModel,
    db: Session = Depends(get_db)
):
    """Create a new pin for an employee."""
    now = datetime.now(UTC)
    status = ""
    employee_id = None
    device_id = None
    timezone = "UTC"
    try:
        employee = await get_employee_by_dni(data.dni, db)
        if not employee:
            raise NotFoundException("Employee not found.")
        employee_id = employee.id
    except Exception as e:
        status += f" {str(e)}"

    try:
        if employee_id and not employee.enrollments:
            raise ValueError("Employee has no enrollments.")

        if employee_id and employee.enrollments and not employee.enrollments.pin:
            raise ValueError("Employee has no pin.")

        if (employee_id and employee.enrollments and employee.enrollments.pin
        and not employee.enrollments.is_same_pin(data.pin)):
            raise ValueError("Invalid PIN.")
    except Exception as e:
        status += f" {str(e)}"

    try:
        device = await get_device_by_id(data.device_id, db)
        if not device:
            raise NotFoundException("Device not found.")
        device_id = device.id
        timezone = device.timezone

        if device.punch_type.pin is False:
            raise ValueError("Invalid punch type on device.")

        if employee_id and device.device_group_id != employee.device_group_id:
            raise ValueError("Invalid device group.")

    except Exception as e:
        status += f" {str(e)}"

    if status == "":
        status = "1"


    punch = Punch(
        device_id=device_id,
        timezone=timezone,
        punch_dtm=now,
        punch_type=PunchTypeEnum.pin,
        dni=data.dni,
        status=status,
        employee_id=employee_id,
        pin=data.pin,
        photo=None,
        in_out=True
    )

    db.add(punch)
    db.commit()
    return {"data": punch}
