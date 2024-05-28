from abc import ABC, abstractmethod


class MessageBroker(ABC):
    @abstractmethod
    async def connect(self):
        pass

    @abstractmethod
    async def close(self):
        pass

    @abstractmethod
    async def declare_queue(self, queue_name: str):
        pass

    @abstractmethod
    async def publish(self, queue_name: str, message: dict):
        pass

    @abstractmethod
    async def consume(self, queue_name: str, callback):
        pass
