from abc import abstractmethod, ABCMeta
from collections import Callable

from core.communication.event import Event


class Connection(metaclass=ABCMeta):
    _on_message: Callable[[str], None]
    _on_close: Callable[[], None] = None

    def __init__(self, on_message: Callable[[str], None]):
        self._on_message = on_message

    def set_on_close(self, on_close: Callable[[], None]):
        self._on_close = on_close

    @abstractmethod
    async def emit(self, event: Event) -> None:
        pass

    @abstractmethod
    async def connect(self) -> None:
        pass

    async def close(self) -> None:
        await self._close()
        if self._on_close:
            self._on_close()

    @abstractmethod
    async def _close(self) -> None:
        pass

    @abstractmethod
    async def is_connected(self) -> bool:
        pass
