from abc import abstractmethod, ABCMeta
from typing import Callable

from core.communication.event import Message


class Connection(metaclass=ABCMeta):

    _on_message: Callable[[str], None] = None
    _on_close: Callable[[], None] = None

    def set_on_close(self, on_close: Callable[[], None]):
        self._on_close = on_close

    def set_on_message(self, on_message: Callable[[str], None]):
        self._on_message = on_message

    @abstractmethod
    async def dispatch(self, event: Message) -> None:
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

    @property
    @abstractmethod
    async def is_connected(self) -> bool:
        pass


class SyncConnection(Connection):

    _on_event: Callable[[Message], None]

    def __init__(self, on_event: Callable[[Message], None]):
        self._on_event = on_event

    async def dispatch(self, event: Message) -> None:
        self._on_event(event)

    async def connect(self) -> None:
        return

    async def _close(self) -> None:
        return

    @property
    async def is_connected(self) -> bool:
        return True


