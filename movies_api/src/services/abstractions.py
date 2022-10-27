from abc import ABC, abstractmethod


class AsyncCacheStorage(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass

    @abstractmethod
    async def set(self, key: str, value: str, **kwargs):
        pass


class FullTextSearch(ABC):
    @abstractmethod
    async def get(self, key: str, **kwargs):
        pass


class AbstractService(ABC):
    @abstractmethod
    async def get_by_id(*args, **kwargs):
        pass

    @abstractmethod
    async def get_list(*args, **kwargs):
        pass

    @abstractmethod
    async def search(*args, **kwargs):
        pass

