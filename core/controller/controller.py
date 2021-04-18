from collections import Callable
from typing import Dict

from core.communication.event import Event
from core.communication.topic import Topic
from core.module.module import Module


class Controller:

    _subscriptions: Dict[Topic, Callable[[Event], None]]
    _modules: Dict[str, Module]

    def __init__(self, subscriptions: Dict[Topic, Callable[[Event], None]], modules: Dict[str, Module]):
        self._modules = modules
        self._subscriptions = subscriptions

    def on_event(self, event: Event):
        """check access permissions, translate event to target or handler"""

    def _setup_modules(self):
        for module_name, module in self._modules.items():
            module.setup()

    def setup(self) -> None:
        pass


