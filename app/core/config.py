from typing import Optional

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"
    KAFKA_BOOTSTRAP_SERVERS: str = "localhost:9092"

    DATABASE_URL: PostgresDsn = "postgresql+asyncpg://user:password@localhost/dbname"
    REDIS_HOST: str = "localhost"

    LOKI_URL: Optional[str] = None
    LOG_LEVEL: str = "INFO"


settings = Settings()
