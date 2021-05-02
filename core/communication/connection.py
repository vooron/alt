from abc import abstractmethod, ABCMeta
from typing import Callable

from core.communication.message import Message


class Connection(metaclass=ABCMeta):

    _on_message: Callable[[str], None] = None
    _on_close: Callable[[], None] = None

    def set_on_close(self, on_close: Callable[[], None]):
        self._on_close = on_close

    def set_on_message(self, on_message: Callable[[str], None]):
        self._on_message = on_message

    @abstractmethod
    def dispatch(self, event: Message) -> None:  # from Ald to connected
        pass

    def send_message(self, message: str) -> None:  # subscribe messages from connected service to Alt
        self._on_message(message)

    @abstractmethod
    def connect(self) -> None:
        pass

    def close(self) -> None:
        self._close()
        if self._on_close:
            self._on_close()

    @abstractmethod
    def _close(self) -> None:
        pass

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        pass


class SyncConnection(Connection):

    _on_event: Callable[[Message], None]

    def __init__(self, on_event: Callable[[Message], None]):
        self._on_event = on_event

    def dispatch(self, event: Message) -> None:
        self._on_event(event)

    def connect(self) -> None:
        return

    def _close(self) -> None:
        return

    @property
    def is_connected(self) -> bool:
        return True


