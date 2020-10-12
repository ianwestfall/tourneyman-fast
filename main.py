import logging

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from api.routers import security
from api.routers.security import get_current_active_user
from api.schemas.security import User

logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

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


@app.get('/users/me', response_model=User, description='Get the current user', tags=['tutorial'])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get('/users/me/items', description='Get the current user\'s items', tags=['tutorial'])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{'item_id': 'Foo', 'owner': current_user.email}]
