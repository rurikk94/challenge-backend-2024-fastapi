import sys
from typing import Annotated, List
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from src.models.schemas import DeviceGroup, Devices, Employee
from src.database.database import get_db
from src.repository.repository import get_all, get_by_id
from src.schemas.schemas import DeviceGroupInputModel, DeviceGroupModel, DeviceGroupsModel, ResponseModel, DeviceGroupDBModel


_device_groups = APIRouter()


@_device_groups.get("/", tags=["device_groups"], response_model=ResponseModel[DeviceGroupsModel])
async def device_groups(db = Depends(get_db)):
    groups = get_all(db, DeviceGroup)
    return {"data": groups}

@_device_groups.post("/", tags=["device_groups"], response_model=ResponseModel[DeviceGroupDBModel])
async def create_device_group(
    group: DeviceGroupInputModel,
    db = Depends(get_db)
):
    return await create_group(group, db)

async def asignar_devices(group_id: int, lst_devices: List[Devices], db: Session):
    for device in lst_devices:
        device.device_group_id = group_id
        db.add(device)
    db.commit()

async def asignar_employees(group_id: int, lst_employees: List[Employee], db: Session):
    for employee in lst_employees:
        employee.device_group_id = group_id
        db.add(employee)
    db.commit()

async def create_group(in_group: DeviceGroupInputModel , db: Session):
    grupo = in_group.model_dump(exclude={"devices", "employees"})
    group = DeviceGroup(**grupo)
    db.add(group)
    db.commit()

    lst_devices: List[int] = in_group.devices
    lst_employees: List[int] = in_group.employees

    devices = get_all(db, Devices, in_=(Devices.id, lst_devices))
    employees =  get_all(db, Employee, in_=(Employee.id, lst_employees))

    await asignar_devices(group.id, devices, db)
    await asignar_employees(group.id, employees, db)
    db.commit()
    return {"data": group}

@_device_groups.get("/{device_group_id}", tags=["device_groups"], response_model=ResponseModel[DeviceGroupDBModel])
async def device_group_by_id(
    device_group_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    db = Depends(get_db)
):
    dg = await get_device_group_by_id(device_group_id, db)
    return {"data": dg}

async def get_device_group_by_id(device_group_id, db) -> DeviceGroupsModel:
    return get_by_id(db, DeviceGroup, device_group_id)