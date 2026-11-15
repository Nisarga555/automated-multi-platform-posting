
from abc import ABC, abstractmethod


class BasePlatform(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def publish(self, message: str) -> dict:
        pass
