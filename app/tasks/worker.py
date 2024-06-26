import asyncio

from app.core.logger import daemon_logger


async def some_background_task():
    while True:
        daemon_logger.info("Performing background task...")
        await asyncio.sleep(5)  # Задержка для имитации выполнения задачи


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(some_background_task())
    loop.run_forever()
