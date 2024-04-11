import sys
from typing import Annotated, List
from fastapi import APIRouter, Depends, Path

from sqlalchemy.orm import Session

from src.models.schemas import DevicePunchType, Devices
from src.database.database import get_db
from src.repository.repository import get_all, get_by_id
from src.schemas.schemas import (
    DevicesDBModel,
    ResponseModel,
    DeviceDBModel,
    DeviceModel,
)


_devices = APIRouter()


@_devices.get("/", tags=["devices"], response_model=ResponseModel[DevicesDBModel])
async def devices(db: Session = Depends(get_db)):
    """Get all devices."""
    devices = get_all(db, Devices)
    return {"data": devices}


@_devices.get(
    "/{device_id}", tags=["devices"], response_model=ResponseModel[DeviceDBModel]
)
async def device_by_id(
    device_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    db: Session = Depends(get_db),
):
    """Get a device by ID."""
    device = await get_device_by_id(device_id, db)
    return {"data": device}


async def get_device_by_id(device_id, db) -> Devices:
    """Get a device by ID."""
    return get_by_id(db, Devices, device_id)


@_devices.post("/", tags=["devices"], response_model=ResponseModel[DeviceDBModel])
async def device_create(device: DeviceModel, db: Session = Depends(get_db)):
    """Create a new device."""

    new_device = Devices(**device.model_dump(exclude=["pin", "face"]))
    db.add(new_device)
    new_device_punch_type = DevicePunchType(
        **device.model_dump(include=["pin", "face"])
    )
    db.flush()
    new_device_punch_type.device_id = new_device.id
    db.add(new_device_punch_type)
    db.commit()

    device = await get_device_by_id(new_device.id, db)
    return {"data": device}


@_devices.put(
    "/{device_id}", tags=["devices"], response_model=ResponseModel[DeviceDBModel]
)
async def device_update(
    device_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    device_data: DeviceModel,
    db: Session = Depends(get_db),
):
    """Update a device."""
    device: Devices = get_by_id(db, Devices, device_id)
    device.update_from_dict(device_data.model_dump(exclude=["pin", "face"]))
    db.commit()
    device_punch_type: DevicePunchType = get_by_id(db, DevicePunchType, device_id)
    device_punch_type.update_from_dict(device_data.model_dump(include=["pin", "face"]))
    db.commit()
    device = await get_device_by_id(device_id, db)
    return {"data": device}


@_devices.delete(
    "/{device_id}", tags=["devices"], response_model=ResponseModel[DeviceDBModel]
)
async def device_delete(
    device_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    db: Session = Depends(get_db),
):
    """Delete a device."""
    device: Devices = get_by_id(db, Devices, device_id)
    d_data = DeviceDBModel.from_orm(device)
    db.delete(device)
    db.commit()
    return {"data": d_data}
