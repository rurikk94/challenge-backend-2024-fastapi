"""This module contains the enroll routes."""

from typing import Annotated
import io
import pickle

from fastapi import APIRouter, Depends, Path, UploadFile
from sqlalchemy.orm import Session

from src.models.schemas import Enrollments
from src.database.database import get_db
from src.schemas.schemas import PinModel, FaceModel, ResponseModel, FaceModel
from .employees import get_employee_by_id

from src.face_recognition import encode_photo

_enroll = APIRouter()


@_enroll.post("/{employee_id}/face", response_model=ResponseModel[FaceModel])
async def create_photo(
    photo: UploadFile,
    employee_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    db: Session = Depends(get_db),
):
    """Create a new photo for an employee."""
    employee = await get_employee_by_id(employee_id, db)

    photo_contents: bytes = await photo.read()
    from PIL import Image

    # Crear una imagen PIL desde los datos
    image_data = io.BytesIO(photo_contents)
    photo_contents = Image.open(image_data).convert("RGB")

    enroll_face = encode_photo(photo_contents)

    b_enroll_face = pickle.dumps(enroll_face)

    if not employee._enrollments:
        enroll = Enrollments(employee_id=employee.id, face=b_enroll_face)
    else:
        enroll = employee._enrollments
        enroll.face = b_enroll_face

    db.add(enroll)
    db.commit()
    return {"data": {"face": True}}


@_enroll.post("/{employee_id}/pin", response_model=ResponseModel[PinModel])
async def create_pin(
    data: PinModel,
    employee_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    db: Session = Depends(get_db),
):
    """Create a new pin for an employee."""
    employee = await get_employee_by_id(employee_id, db)

    if not employee._enrollments:
        enroll = Enrollments(employee_id=employee.id, pin=data.pin)
    else:
        enroll = employee._enrollments
        enroll.pin = data.pin

    db.add(enroll)
    db.commit()
    return {"data": enroll}
