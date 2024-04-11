from datetime import date
from typing import Annotated
from fastapi import APIRouter, Depends, Path

from src.models.schemas import Timecard
from src.database.database import get_db
from src.repository.repository import get_all
from src.schemas.schemas import ResponseModel, TimecardModel


_timecards = APIRouter()


@_timecards.get(
    "/{employee_id}", tags=["timecards"], response_model=ResponseModel[TimecardModel]
)
async def timecard_by_employee_id(
    employee_id: Annotated[int, Path(title="The ID of the item to get", gt=0)],
    start: date,
    end: date,
    db=Depends(get_db),
):
    return await get_timecard_by_employee_id(employee_id, start, end, db)


async def get_timecard_by_employee_id(employee_id: int, start: date, end: date, db):
    timecard: TimecardModel = get_all(
        db, Timecard, employee_id=employee_id, between=[Timecard.date, start, end]
    )
    return {"data": timecard}
