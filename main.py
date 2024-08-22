from typing import Any, Dict, List
from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import ResponseValidationError
from fastapi.responses import JSONResponse


from models.schemas import Trade, User


app = FastAPI(title="App for trade")


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(
    request: Request, exception: ResponseValidationError
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exception.errors()}),
    )


fake_users = [
    {"id": 1, "role": "admin", "name": "alex"},
    {"id": 2, "role": "investor", "name": "bob"},
    {"id": 3, "role": "trader", "name": "pol"},
    {
        "id": 4,
        "role": "investor",
        "name": "mike",
        "degree": [
            {"id": 1, "created_at": "2024-08-21T00:00:00", "type": "expert"}
        ],
    },
]

fake_trades = [
    {
        "id": 1,
        "user_id": 1,
        "currency": "BTC",
        "side": "buy",
        "price": 300,
        "amount": 3.65,
    },
    {
        "id": 2,
        "user_id": 1,
        "currency": "BTC",
        "side": "sell",
        "price": 347,
        "amount": 3.65,
    },
]


@app.get("/users/{user_id}", response_model=List[User])
async def get_user(user_id: int) -> List[Dict[str, Any]]:
    return [user for user in fake_users if user.get("id") == int(user_id)]


@app.post("/trades")
async def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}

