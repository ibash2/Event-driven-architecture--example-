import asyncio
import signal
from contextlib import asynccontextmanager


from fastapi import FastAPI, Depends

from app.tasks.consumer import consume
from app.tasks.worker import some_background_task
# from app.core.logger import logger

from app.core.config import settings
from app.api.router import router as orders_router
from app.services.rabbitmq_service import RabbitMQBroker

# from app.services.kafka_service import KafkaBroker

# from app.database import Base, engine


# Выберите нужный брокер (RabbitMQ или Kafka)
rabbitmq = RabbitMQBroker(settings.RABBITMQ_URL)
# kafka = KafkaBroker(settings.KAFKA_BOOTSTRAP_SERVERS)

broker = rabbitmq
# broker = kafka


@asynccontextmanager
async def lifespan(app: FastAPI):
    cons = asyncio.create_task(consume())
    await broker.connect()
    await broker.declare_queue("order_created")

    yield
    await broker.close()


app = FastAPI(lifespan=lifespan)
app.state.broker = broker

# Передача брокера в маршрутизаторы
app.include_router(
    orders_router,
    prefix="/orders",
    tags=["orders"],
)


async def main():
    await asyncio.create_task(consume())


def shutdown(loop, signal=None):
    # logger.info(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    loop.stop()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # for sig in (signal.SIGINT, signal.SIGTERM):
    #     loop.add_signal_handler(sig, shutdown, loop, sig)

    try:
        asyncio.run(main())
    except (SystemExit, KeyboardInterrupt):
        # logger.info("Service is shutting down...")
        pass
