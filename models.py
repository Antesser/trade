from pydantic import BaseModel


class Trade(BaseModel):
    id:int
    user_id:int
    currency:str
    side: str
    price: int
    amount: float