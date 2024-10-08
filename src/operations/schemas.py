from datetime import datetime

from pydantic import BaseModel


class OperationCreate(BaseModel):
    id: int
    quantity: int
    figi: str
    instrument_type: str
    date: datetime
    type: str
