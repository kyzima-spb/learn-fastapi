from __future__ import annotations
import typing as t

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pythoninfo import pythoninfo

from .database import Base, get_db, engine
from . import models
from .oauth2 import router as oauth2_router
from .routes import genres
from .routes import users


def create_app() -> FastAPI:
    app = FastAPI(
        title='Game Store API',
        description='An example of a REST API for a game store.',
    )
    app.include_router(oauth2_router)
    app.include_router(genres.router)
    app.include_router(users.router)

    @app.get('/', summary='About the environment')
    def index() -> HTMLResponse:
        """Shows information about the environment."""
        return HTMLResponse(pythoninfo())

    return app
