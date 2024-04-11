"""This module contains the enroll routes."""

import base64
from datetime import datetime
from io import BytesIO
from typing import Annotated
from fastapi import APIRouter, Depends, Form, UploadFile
from sqlalchemy.orm import Session

from src.models.schemas import Punch, PunchTypeEnum
from src.database.database import get_db
from src.schemas.schemas import (
    PunchPinModel,
    ResponseModel,
    PunchDBModel,
    PunchPhotoModel,
)
from .employees import get_employee_by_dni
from .devices import get_device_by_id
from src.exceptions import NotFoundException

from PIL import Image

_punch = APIRouter()


@_punch.post("/face", response_model=ResponseModel[PunchDBModel])
async def create_punch_photo(
    # data: PunchPhotoModel,
    photo: Annotated[UploadFile | str, Form()],
    dni: Annotated[str, Form()],
    device_id: Annotated[int, Form()],
    db: Session = Depends(get_db),
):
    """Create a new photo punch for an employee."""
    now = datetime.utcnow()
    status = ""
    employee_id = None
    # device_id = None
    timezone = "UTC"

    try:
        employee = await get_employee_by_dni(dni, db)
        if not employee:
            raise NotFoundException("Employee not found.")
        employee_id = employee.id
    except Exception as e:
        status += f" {str(e)}"

    if isinstance(photo, str):
        # Decodificar la cadena base64
        decoded_data = base64.b64decode(photo.split(",")[1])

        # Convertir los datos decodificados en un objeto BytesIO
        image_data = BytesIO(decoded_data)

        # Crear una imagen PIL desde los datos
        photo_contents = Image.open(image_data).convert("RGB")
    else:
        photo_contents: bytes = await photo.read()
        image_data = BytesIO(photo_contents)
        photo_contents = Image.open(image_data).convert("RGB")

    try:
        if employee_id and not employee.has_enrollments():
            raise ValueError("Employee has no enrollments.")

        if (
            employee_id
            and employee.has_enrollments()
            and not employee.has_face_enrollment()
        ):
            raise ValueError("Employee has no photo.")

        if (
            employee_id
            and employee.has_enrollments()
            and employee.has_face_enrollment()
            and not employee.has_same_face(photo_contents)
        ):
            raise ValueError("Face dont match.")
    except Exception as e:
        status += f" {str(e)}"

    try:
        device = await get_device_by_id(device_id, db)
        if not device:
            raise NotFoundException("Device not found.")
        device_id = device.id
        timezone = device.timezone

        if device.punch_type.face is False:
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
        punch_type=PunchTypeEnum.face,
        dni=dni,
        status=status,
        employee_id=employee_id,
        pin=None,
        photo=None,
        in_out=True,
    )

    db.add(punch)
    db.commit()
    return {"data": punch}


@_punch.post("/pin", response_model=ResponseModel[PunchDBModel])
async def create_punch(data: PunchPinModel, db: Session = Depends(get_db)):
    """Create a new pin for an employee."""
    now = datetime.utcnow()
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
        if employee_id and not employee.has_enrollments():
            raise ValueError("Employee has no enrollments.")

        if (
            employee_id
            and employee.has_enrollments()
            and not employee.has_pin_enrollment()
        ):
            raise ValueError("Employee has no pin.")

        if (
            employee_id
            and employee.has_enrollments()
            and employee.has_pin_enrollment()
            and not employee.has_same_pin(data.pin)
        ):
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
        in_out=True,
    )

    db.add(punch)
    db.commit()
    return {"data": punch}
