import logging
from typing import Dict, Callable

from controller.client import Event
from core.communication.command_identifier import CommandIdentifier
from core.controller.controller import Controller
from core.module.impl.gui.module import UIModule
from core.module.impl.text_indexer.module import TextIndexerModule
from core.module.impl.text_to_command.module import TextToCommandModule
from core.module.module import Module

logging.basicConfig(level=logging.INFO)

subscriptions: Dict[CommandIdentifier, Callable[[Event], None]] = {
    CommandIdentifier("core", "userFlow", "wakeUp"): ...,
    CommandIdentifier("core", "userFlow", "callCommandFromQuery"): ...
}

modules: Dict[str, Module] = {
    "UI": UIModule(),
    "TextIndexer": TextIndexerModule(),  # Used to index config data + each query
    "TextToCommand": TextToCommandModule(),  # Recommend top N commands to execute according to query.
}

if __name__ == "__main__":
    controller = Controller(
        subscriptions=subscriptions,
        modules=modules
    )

    controller.setup()



