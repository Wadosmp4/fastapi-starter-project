import logging
from logging.config import dictConfig
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.config import LogConfig


dictConfig(LogConfig().dict())
logger = logging.getLogger('app')

app = FastAPI()


@app.get('/')
def read_root() -> dict[str, str]:
    return {'message': 'Welcome to FastAPI Starter!'}


def custom_openapi() -> dict[str, Any]:
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title='Documentation',
        version='1.0.0',
        description='Docs for Starter Project',
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema
    return app.openapi_schema


setattr(app, 'openapi', custom_openapi)
