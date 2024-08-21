from typing import Any, List
from fastapi import FastAPI

from models import Trade


app = FastAPI(title="App for trade")

fake_users = [
    {"id": 1, "role": "admin", "name": "alex"},
    {"id": 2, "role": "investor", "name": "bob"},
    {"id": 3, "role": "trader", "name": "pol"},
]


@app.get("/users/{user_id}")
async def get_user(user_id: int) -> list[dict[str, Any]]:
    return [user for user in fake_users if user.get("id") == int(user_id)]


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


@app.post("/trades")
async def add_trades(trades: List[Trade]):
    fake_trades.extend(trades)
    return {"status": 200, "data": fake_trades}