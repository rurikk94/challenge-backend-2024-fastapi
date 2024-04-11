from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware

from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from src.schemas.schemas import LoginModel
from src.database import Base, engine
from src.config import config
from src.models import *
from src.routes import _v1

app = FastAPI(
    title=config.app_name,
    version=config.app_version,
    servers=[{"url": f"http://127.0.0.1:{config.port}/"}],
    debug=config.debug,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=config.cors_allow_credentials,
    allow_methods=config.cors_allow_methods,
    allow_headers=config.cors_allow_headers,
)

app.include_router(_v1, prefix="/v1")

Base.metadata.create_all(bind=engine)

from starlette.requests import Request as StarletteRequest


@app.exception_handler(Exception)
async def exception_handler(request: StarletteRequest, exc: Exception):
    # print(traceback.format_exc())
    print(f"{request.method=} {request.url=}")
    return JSONResponse(
        content={"status": "error", "message": jsonable_encoder(str(exc))},
        status_code=exc.status_code,
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: StarletteRequest, exc: Exception):
    # print(traceback.format_exc())
    print(f"{request.method=} {request.url=}")
    return JSONResponse(
        content={"status": "error", "message": jsonable_encoder(exc.detail)},
        status_code=exc.status_code,
    )
