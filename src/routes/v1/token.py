import sys
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path

from src.models.schemas import Employee
from src.database.database import get_db
from src.repository.repository import get_all, get_by_id
from src.schemas.schemas import TokenModel, ResponseModel, LoginModel

import uuid

_token = APIRouter()

@_token.post("/", response_model=ResponseModel[TokenModel])
async def token(data: LoginModel):
    if data.username != "admin":
        raise HTTPException(status_code=401, detail="Usuario no autorizado")
    return {"data": {"token": uuid.uuid4().hex }}