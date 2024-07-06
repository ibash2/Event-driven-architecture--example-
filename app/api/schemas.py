from typing import Optional

from app.utils.base_model import CustomModel

from pydantic import BaseModel


class OrderCreate(BaseModel):
    item: str
    quantity: int
    id: Optional[int] = None


class OrderResponse(BaseModel):
    id: int
    item: str
    quantity: int
