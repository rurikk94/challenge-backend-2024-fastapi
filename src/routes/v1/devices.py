import sys
from typing import Annotated, List
from fastapi import APIRouter, Depends, Path

from src.models.schemas import Devices
from src.database.database import get_db
from src.repository.repository import get_all, get_by_id
from src.schemas.schemas import DevicesDBModel, ResponseModel, DeviceDBModel


_devices = APIRouter()


@_devices.get("/", tags=["devices"], response_model=ResponseModel[DevicesDBModel])
async def devices(db = Depends(get_db)):
    devices = get_all(db, Devices)
    return {"data": devices}

@_devices.get("/{device_id}", tags=["devices"], response_model=ResponseModel[DeviceDBModel])
async def device_group_by_id(
    device_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    db = Depends(get_db)
):
    return await get_device_by_id(device_id, db)


async def get_device_by_id(device_group_id, db):
    device: DevicesDBModel = get_by_id(db, Devices, device_group_id)
    return {"data": device}