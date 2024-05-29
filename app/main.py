from fastapi import FastAPI, Depends

from app.core.config import settings
from app.api.router import router as orders_router
from app.services.rabbitmq_service import RabbitMQBroker

# from app.services.kafka_service import KafkaBroker

# from app.database import Base, engine

app = FastAPI()

# Выберите нужный брокер (RabbitMQ или Kafka)
rabbitmq = RabbitMQBroker(settings.RABBITMQ_URL)
# kafka = KafkaBroker(settings.KAFKA_BOOTSTRAP_SERVERS)

broker = rabbitmq
# broker = kafka


@app.on_event("startup")
async def startup_event():
    await broker.connect()
    await broker.declare_queue("order_created")


@app.on_event("shutdown")
async def shutdown_event():
    await broker.close()


# Передача брокера в маршрутизаторы
app.include_router(
    orders_router,
    prefix="/orders",
    tags=["orders"],
    dependencies=[Depends(lambda: broker)],
)


# import asyncio
# import signal
# from app.tasks.consumer import consume
# from app.tasks.worker import some_background_task
# from app.core.logger import logger


# async def main():
#     consume_task = asyncio.create_task(consume())
#     worker_task = asyncio.create_task(some_background_task())

#     await asyncio.gather(consume_task, worker_task)


# def shutdown(loop, signal=None):
#     logger.info(f"Received exit signal {signal.name}...")
#     tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
#     [task.cancel() for task in tasks]
#     loop.stop()


# if __name__ == "__main__":
#     loop = asyncio.get_event_loop()

#     for sig in (signal.SIGINT, signal.SIGTERM):
#         loop.add_signal_handler(sig, shutdown, loop, sig)

#     try:
#         asyncio.run(main())
#     except (SystemExit, KeyboardInterrupt):
#         logger.info("Service is shutting down...")
