import logging
from typing import Dict

from core.application.application import Application
from core.application.impl.user_query_processing import UserQueryProcessing
from core.controller.controller import Controller
from core.module.impl.gui.module import UIModule
from core.module.impl.text_indexer.module import TextIndexerModule
from core.module.impl.text_to_command.module import TextToCommandModule
from core.module.module import Module

logging.basicConfig(level=logging.INFO)

modules: Dict[str, Module] = {
    "UI": UIModule("UI"),
    "TextIndexer": TextIndexerModule("TextIndexer"),  # Used to index config data + each query
    "TextToCommand": TextToCommandModule("TextToCommand"),  # Recommend top N commands to execute according to query.
}

applications: Dict[str, Application] = {
    "UserQueryProcessing": UserQueryProcessing("UserQueryProcessing")
}

if __name__ == "__main__":
    controller = Controller(
        modules=modules,
        applications=applications
    )

    controller.setup()
