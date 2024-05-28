from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, Order
from app.utils.message_broker import MessageBroker

from app.api.schemas import OrderCreate, OrderResponse

router = APIRouter()


@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
    broker: MessageBroker = Depends(),
):
    new_order = Order(item=order.item, quantity=order.quantity)
    db.add(new_order)
    await db.commit()
    await db.refresh(new_order)
    await broker.publish(
        "order_created",
        {"id": new_order.id, "item": new_order.item, "quantity": new_order.quantity},
    )
    return new_order


@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id)
    return order
