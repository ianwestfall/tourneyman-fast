import logging
from logging.config import fileConfig

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import security, tournament, stage, competitor

fileConfig('logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)


app = FastAPI(
    title='Tourneyman',
    description='Open-source tournament management software',
    version='0.0.1',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        'http://localhost:8080',
        'https://localhost:8080',
    ],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(security.router, prefix='/auth', tags=['authentication'])
app.include_router(tournament.router)
app.include_router(stage.router)
app.include_router(competitor.router)
