import base64
from datetime import datetime, date, time, timezone
import enum
import io
from typing import List, Optional
from sqlalchemy import Boolean, Column, Date, DateTime, ForeignKey, Integer, String, Time, Enum
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.dialects.postgresql import BYTEA

import pytz

from src.database.database import Base
import src.face_recognition as fr
from PIL import Image

class Employee(Base):
    __tablename__ = "employee"

    id:         Mapped[int] =    Column(Integer, primary_key=True, index=True)
    dni:        Mapped[str] =    Column(String, nullable=False)
    fullname:   Mapped[str] =    Column(String, nullable=False)
    email:      Mapped[str] =    Column(String, nullable=False)
    device_group_id: Mapped[int] = Column(Integer, ForeignKey("device_group.id"), nullable=True)

    _device_group: Mapped[Optional["DeviceGroup"]] = relationship("DeviceGroup", uselist=False, passive_deletes=True, cascade="all, delete")

    _punchs: Mapped[List["Punch"]] = relationship("Punch")

    @property
    def device_group(self):
        if self._device_group is None:
            return None
        return self._device_group.name

    _enrollments: Mapped[Optional["Enrollments"]] = relationship("Enrollments", uselist=False)

    def has_enrollments(self) -> bool:
        return True if self._enrollments else False

    def has_face_enrollment(self) -> bool:
        return True if self._enrollments.face else False

    def has_pin_enrollment(self) -> bool:
        return True if self._enrollments.pin else False

    def has_same_face(self, punch_photo: bytes) -> bool:
        return self._enrollments.is_same_photo(punch_photo)

    def has_same_pin(self, pin: str | int) -> bool:
        return self._enrollments.is_same_pin(pin)

    @property
    def enrollments(self):
        if self._enrollments:
            face = True if self._enrollments.face else False
            return {
                "employee_id": self._enrollments.employee_id,
                "pin": self._enrollments.pin,
                "face": face
                }
        return None

    @enrollments.setter
    def enrollments(self, value):
        self._enrollments = value



class Enrollments(Base):
    __tablename__ = "enrollments"

    employee_id: Mapped[int] =     Column(Integer, ForeignKey("employee.id"), primary_key=True)
    pin:         Mapped[Optional[str]] =     Column(String, nullable=True)
    face:        Mapped[Optional[bytes]] =   Column(BYTEA, nullable=True)

    def is_same_pin(self, pin: str | int) -> bool:
        pin = int(pin) if isinstance(pin, str) else pin
        return int(self.pin) == pin

    def is_same_photo(self, punch_photo: bytes) -> bool:
        def porcentaje_true(lista: List[bool]):
            total = len(lista)
            true_count = sum(1 for elemento in lista if elemento)  # Contar cuántos elementos son True
            porcentaje = (true_count / total) * 100
            return porcentaje


        # image = Image.open(image).convert("RGB")
        # image = Image.frombytes("RGB", (640, 480), punch_photo)
        # image = Image.open(io.BytesIO(base64.b64decode(punch_photo)))


        punch_face = fr.encode_photo(punch_photo)
        import pickle
        enroll = pickle.loads(self.face)
        match: List[bool] = fr.match(punch_face, enroll)
        if porcentaje_true(match) >= 70:
            return True
        return False

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
    device_group_id: Mapped[int] = Column(Integer, ForeignKey("device_group.id"), nullable=True)

    punch_type: Mapped["DevicePunchType"] = relationship("DevicePunchType", uselist=False, passive_deletes=True, cascade="all, delete")

    _device_group: Mapped["DeviceGroup"] = relationship("DeviceGroup", uselist=False, passive_deletes=True, cascade="all, delete")

    @property
    def pin(self):
        return self.punch_type.pin

    @property
    def face(self):
        return self.punch_type.face

    @property
    def device_group(self):
        if self._device_group is None:
            return None
        return self._device_group.name

    @device_group.setter
    def device_group(self, value):
        self.device_group_id = value

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
    pin:         Mapped[Optional[str]] =       Column(String, nullable=True)
    photo:       Mapped[Optional[bytes]] =     Column(BYTEA, nullable=True)
    in_out:      Mapped[bool] =                 Column(Boolean, default=True)

    @property
    def _local_tz(self):
        return pytz.timezone(self.timezone)

    @property
    def punch_dtm_local(self) -> datetime:
        return self.punch_dtm.replace(tzinfo=timezone.utc).astimezone(tz=self._local_tz)