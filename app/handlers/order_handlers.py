import json
from app.utils.event_decorator import event_handler
from app.database import get_db, Order, SessionLocal
from app.core.logger import order_logger


@event_handler("order_created")
async def handle_order_created(message):
    async with SessionLocal() as db:
        order_data = json.loads(message.body)
        order = Order(
            id=order_data["id"],
            item=order_data["item"],
            quantity=order_data["quantity"],
        )
        db.add(order)
        await db.commit()
        order_logger.info(f"Processed order: {order_data}")
    await message.ack()


@event_handler("order_updated")
async def handle_order_updated(message):
    async with get_db() as db:
        order_data = json.loads(message.body)
        order = await db.get(Order, order_data["id"])
        order.item = order_data["item"]
        order.quantity = order_data["quantity"]
        await db.commit()
        order_logger.info(f"Updated order: {order_data}")
    await message.ack()
