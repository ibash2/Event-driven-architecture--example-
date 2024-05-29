import asyncio

from app.services.rabbitmq_service import RabbitMQBroker
# from app.services.kafka_service import KafkaBroker

from app.core.config import settings
from app.utils.event_decorator import get_handler
from app.core.logger import consumer_logger


async def handle_message(message):
    event_type = message.headers.get("event_type")
    handler = get_handler(event_type)
    if handler:
        await handler(message)
    else:
        consumer_logger.warning(f"No handler for event type: {event_type}")
        await message.ack()


async def consume():
    rabbitmq = RabbitMQBroker(settings.RABBITMQ_URL)
    await rabbitmq.connect()
    await rabbitmq.consume("order_events", handle_message)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(consume())
