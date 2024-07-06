import json

import aio_pika
from aio_pika import Message

from app.utils.message_broker import MessageBroker


class RabbitMQBroker(MessageBroker):
    def __init__(self, amqp_url: str):
        self.amqp_url = amqp_url
        self.connection = None
        self.channel = None

    async def connect(self):
        self.connection = await aio_pika.connect_robust(self.amqp_url)
        self.channel = await self.connection.channel()

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def declare_queue(self, queue_name: str):
        await self.channel.declare_queue(queue_name, durable=True)

    async def publish(self, queue_name: str, message: dict, headers: dict = None):
        if not headers:
            headers = {}
        await self.channel.default_exchange.publish(
            Message(
                body=json.dumps(message).encode(),
                headers=headers,
            ),
            routing_key=queue_name,
        )

    async def consume(self, queue_name: str, callback):
        queue = await self.channel.declare_queue(queue_name, durable=True)
        await queue.consume(callback)
