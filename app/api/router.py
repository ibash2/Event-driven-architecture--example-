from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db, Order
from app.utils.message_broker import MessageBroker
from app.services.rabbitmq_service import RabbitMQBroker

from app.api.schemas import OrderCreate, OrderResponse

router = APIRouter()


@router.post("/", response_model=OrderResponse)
async def create_order(
    request: Request,
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
):
    broker = request.app.state.broker
    new_order = OrderResponse(id=order.id, item=order.item, quantity=order.quantity)
    # db.add(new_order)
    # await db.refresh(new_order)
    await broker.publish(
        "order_events",
        {"id": new_order.id, "item": new_order.item, "quantity": new_order.quantity},
        headers={"event_type": "order_created"},
    )
    return new_order


@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(order_id: int, db: AsyncSession = Depends(get_db)):
    order = await db.get(Order, order_id)
    return order
