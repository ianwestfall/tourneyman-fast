from fastapi import FastAPI, Depends

from api.routers import security
from api.routers.security import get_current_active_user
from api.schemas.security import User

app = FastAPI(
    title='Tourneyman',
    description='Open-source tournament management software',
    version='0.0.1',
)


app.include_router(security.router, prefix='/auth', tags=['authentication'])


@app.get('/users/me', response_model=User, description='Get the current user', tags=['tutorial'])
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get('/users/me/items', description='Get the current user\'s items', tags=['tutorial'])
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{'item_id': 'Foo', 'owner': current_user.email}]
