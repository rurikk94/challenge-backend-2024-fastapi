from fastapi import APIRouter

from src.routes.v1.token import _token
from src.routes.v1.devices import _devices
from src.routes.v1.device_groups import _device_groups
from src.routes.v1.employees import _employees
from src.routes.v1.enroll import _enroll
from src.routes.v1.timecards import _timecards
from src.routes.v1.punch import _punch
from src.config import config


_v1 = APIRouter()

_v1.include_router(_token, prefix="/token")
_v1.include_router(_device_groups, prefix="/device_groups")
_v1.include_router(_devices, prefix="/devices")
_v1.include_router(_employees, prefix="/employees")
_v1.include_router(_enroll, prefix="/enroll")
_v1.include_router(_timecards, prefix="/timecards")
_v1.include_router(_punch, prefix="/punch")


@_v1.get("/version")
async def version():
    """Return the version of the API."""
    return config.version
