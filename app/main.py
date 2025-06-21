import logging
from logging.config import dictConfig
from typing import Any

from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from app.config import LogConfig
from app.routers import (
    categories,
    comments,
    posts,
    profiles,
    relationships_demo,
    roles,
    users,
)


dictConfig(LogConfig().dict())
logger = logging.getLogger('app')

app = FastAPI()

# Include routers
app.include_router(relationships_demo.router, prefix='/api/v1')
app.include_router(users.router, prefix='/api/v1')
app.include_router(posts.router, prefix='/api/v1')
app.include_router(comments.router, prefix='/api/v1')
app.include_router(categories.router, prefix='/api/v1')
app.include_router(roles.router, prefix='/api/v1')
app.include_router(profiles.router, prefix='/api/v1')


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


app.openapi = custom_openapi
