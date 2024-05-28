from typing import Optional

from app.utils.base_model import CustomModel


class OrderCreate(CustomModel):
    item: str
    quantity: int
    id: Optional[int] = None


class OrderResponse(CustomModel):
    id: int
    item: str
    quantity: int
