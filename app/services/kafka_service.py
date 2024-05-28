import json

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from app.utils.message_broker import MessageBroker


class KafkaBroker(MessageBroker):
    def __init__(self, bootstrap_servers: str):
        self.bootstrap_servers = bootstrap_servers
        self.producer = None
        self.consumer = None

    async def connect(self):
        self.producer = AIOKafkaProducer(bootstrap_servers=self.bootstrap_servers)
        await self.producer.start()

    async def close(self):
        if self.producer:
            await self.producer.stop()
        if self.consumer:
            await self.consumer.stop()

    async def declare_queue(self, queue_name: str):
        # В Kafka нет необходимости явно объявлять очереди
        pass

    async def publish(self, queue_name: str, message: dict):
        await self.producer.send_and_wait(queue_name, json.dumps(message).encode())

    async def consume(self, queue_name: str, callback):
        self.consumer = AIOKafkaConsumer(
            queue_name, bootstrap_servers=self.bootstrap_servers, group_id="my-group"
        )
        await self.consumer.start()
        async for msg in self.consumer:
            await callback(msg)
