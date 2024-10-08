from fastapi import Depends, FastAPI


from src.auth.base_config import auth_backend, fastapi_users, current_user
from src.auth.schemas import UserCreate, UserRead
from src.auth.models import User

app = FastAPI(title="App for trade")


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