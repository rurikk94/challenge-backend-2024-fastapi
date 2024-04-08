from datetime import datetime, date, time, timezone
import enum
from typing import List, Optional
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Time, Enum
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.dialects.postgresql import BYTEA

import pytz

from src.database.database import Base

class Employee(Base):
    __tablename__ = "employee"

    id:         Mapped[int] =    Column(Integer, primary_key=True, index=True)
    dni:        Mapped[str] =    Column(String)
    fullname:   Mapped[str] =    Column(String)
    email:      Mapped[str] =    Column(String)
    device_group_id: Mapped[int] = Column(Integer, ForeignKey("device_group.id"))

    _device_group: Mapped["DeviceGroup"] = relationship("DeviceGroup", uselist=False)

    _punchs: Mapped[List["Punch"]] = relationship("Punch")

    @property
    def device_group(self):
        return self._device_group.name

    enrollments: Mapped["Enrollments"] = relationship("Enrollments", uselist=False)

class Enrollments(Base):
    __tablename__ = "enrollments"

    employee_id: Mapped[int] =     Column(Integer, ForeignKey("employee.id"), primary_key=True)
    pin:         Mapped[Optional[str]] =     Column(String)
    face:        Mapped[Optional[bytes]] =   Column(BYTEA)

class DeviceGroup(Base):
    __tablename__ = "device_group"

    id:         Mapped[int] =    Column(Integer, primary_key=True, index=True)
    name:       Mapped[str] =    Column(String)
    description: Mapped[str] =  Column(String)
    _devices:   Mapped[List["Devices"]] = relationship("Devices")
    _employees: Mapped[List["Employee"]] = relationship("Employee")

    @property
    def devices(self) -> int:
        return len(self._devices)

    @property
    def id_devices(self) -> List[int]:
        return [device.id for device in self._devices]

    @property
    def employees(self) -> int:
        return len(self._employees)

    @property
    def id_employees(self) -> List[int]:
        return [employee.id for employee in self._employees]


class Devices(Base):
    __tablename__ = "devices"

    id:         Mapped[int] =    Column(Integer, primary_key=True, index=True)
    name:       Mapped[str] =    Column(String)
    location:   Mapped[str] =    Column(String)
    timezone:   Mapped[str] =    Column(String)
    device_group_id: Mapped[int] = Column(Integer, ForeignKey("device_group.id"))

    punch_type: Mapped["DevicePunchType"] = relationship("DevicePunchType", uselist=False)

    __device_group: Mapped["DeviceGroup"] = relationship("DeviceGroup", uselist=False)

    @property
    def pin(self):
        return self.punch_type.pin

    @property
    def face(self):
        return self.punch_type.face

    @property
    def device_group(self):
        return self.__device_group.name

class DevicePunchType(Base):
    __tablename__ = "punch_type"

    device_id: Mapped[int] =   Column(Integer, ForeignKey("devices.id"), primary_key=True)
    pin:      Mapped[bool] =   Column(Boolean)
    face:     Mapped[bool] =   Column(Boolean)

class Timecard(Base):
    __tablename__ = "timecard"

    id:          Mapped[int] =  Column(Integer, primary_key=True, index=True)
    date:        Mapped["date"] =  Column(Date)
    employee_id: Mapped[int] =  Column(Integer, ForeignKey("employee.id"))
    shift_in:    Mapped[time] =  Column(Time)
    shift_out:   Mapped[time] =  Column(Time)

    @property
    def shifts(self):
        return f"{self.shift_in} - {self.shift_out}"

    employee: Mapped["Employee"] = relationship("Employee", uselist=False)


    @property
    def punch_in(self) -> List[datetime]:
        return [punch.punch_dtm_local for punch in self.employee._punchs if punch.in_out == True and punch.punch_dtm.date() == self.date]

    @property
    def punch_out(self) -> List[datetime]:
        return [punch.punch_dtm_local for punch in self.employee._punchs if punch.in_out == False and punch.punch_dtm.date() == self.date]

class PunchTypeEnum(str, enum.Enum):
    pin = "pin"
    face = "face"

class Punch(Base):
    __tablename__ = "punch"

    id:          Mapped[int] =                 Column(Integer, primary_key=True, index=True)
    device_id:   Mapped[int] =                 Column(Integer, ForeignKey("devices.id"))
    timezone:    Mapped[str] =                 Column(String)
    punch_dtm:   Mapped[datetime] =            Column(DateTime)
    punch_type:  Mapped[PunchTypeEnum] =       Column(Enum(PunchTypeEnum))
    dni:         Mapped[str] =                 Column(String)
    status:      Mapped[str] =                 Column(String)
    employee_id: Mapped[Optional[int]] =       Column(Integer, ForeignKey("employee.id"))
    pin:         Mapped[Optional[str]] =       Column(String)
    photo:       Mapped[Optional[bytes]] =     Column(BYTEA)
    in_out:      Mapped[bool] =                 Column(Boolean, default=True)

    @property
    def _local_tz(self):
        return pytz.timezone(self.timezone)

    @property
    def punch_dtm_local(self) -> datetime:
        return self.punch_dtm.replace(tzinfo=timezone.utc).astimezone(tz=self._local_tz)