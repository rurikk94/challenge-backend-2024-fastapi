
from typing import Generic, List, Optional, TypeVar
from pydantic import AliasPath, BaseModel, Field
from datetime import date, datetime

from src.models.schemas import PunchTypeEnum


M = TypeVar("M", bound=BaseModel)

class ResponseModel(BaseModel, Generic[M]):
    status: Optional[str] = "success"
    data: List[M] | M


class LoginModel(BaseModel):
    username: str
    password: str

class DeviceGroupsModel(BaseModel):
    id: int
    name: str
    description: str
    devices: int
    employees: int

class DeviceGroupModel(BaseModel):
    name: str
    description: str
    devices: List[int]   = Field(serialization_alias='devices', validation_alias='id_devices')
    employees: List[int] = Field(serialization_alias='employees', validation_alias='id_employees')

class DeviceGroupInputModel(DeviceGroupModel):
    devices: List[int]
    employees: List[int]

class DeviceGroupDBModel(DeviceGroupModel):
    id: int

class PunchTypeValuesModel(BaseModel):
    pin: Optional[str]
    face: Optional[bytes]

class PunchTypeModel(BaseModel):
    pin: bool
    face: bool

class DevicesDBModel(BaseModel):
    id: int
    name: str
    location: str
    timezone: str
    device_group: str
    punch_type: PunchTypeModel

class DeviceModel(PunchTypeModel, BaseModel):
    name: str
    location: str
    timezone: str
    device_group: int = Field(validation_alias='device_group_id' )

class DeviceDBModel(DeviceModel):
    id: int

class PunchPinModel(BaseModel):
    dni: str
    pin: str

class PunchPhotoModel(BaseModel):
    dni: str
    photo: bytes

class EmployeeDataModel(BaseModel):
    dni: str
    fullname: str
    email: str

class TokenModel(BaseModel):
    token: str

class EmployeeDBModel(EmployeeDataModel, BaseModel):
    id: int
    enrollments: PunchTypeValuesModel
    device_group_id: int
    device_group: str

class DniModel(BaseModel):
    dni: str

class PhotoModel(BaseModel):
    photo: bytes

class TimecardModel(BaseModel):
    id: int
    date: date
    shifts: str
    punch_in: List[datetime]
    punch_out: List[datetime]

class PunchModel(BaseModel):
    id: int
    device_id: int
    timezone: str
    punch_dtm: datetime
    punch_type: PunchTypeEnum
    dni: str
    status: str
    employee_id: Optional[int]
    pin: Optional[str]
    photo: Optional[bytes]