from app.services.rabbitmq_service import RabbitMQBroker

# from app.services.kafka_service import KafkaBroker
from app.core.config import settings
from app.database import get_db, Order

import asyncio
import json


async def message_callback(message):
    async with get_db() as db:
        order_data = json.loads(message.body)
        order = Order(
            id=order_data["id"],
            item=order_data["item"],
            quantity=order_data["quantity"],
        )
        db.add(order)
        await db.commit()
    await message.ack()


async def consume():
    rabbitmq = RabbitMQBroker(settings.RABBITMQ_URL)
    await rabbitmq.connect()
    await rabbitmq.consume("order_created", message_callback)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
