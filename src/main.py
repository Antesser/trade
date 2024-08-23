from fastapi import Depends, FastAPI
import uvicorn


from auth.base_config import auth_backend, fastapi_users, current_user
from auth.schemas import UserCreate, UserRead
from auth.models import User
from operations.router import router as router_ops
from tasks.router import router as router_tasks
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(title="App for trade", lifespan=lifespan)


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


@app.get("/unprotected-route")
def unprotected_route():
    return "Hello, man"


app.include_router(router_ops)
app.include_router(router_tasks)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
