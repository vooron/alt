import logging
from typing import Dict

from core.controller.controller import Controller
from core.module.impl.text_indexer.module import TextIndexerModule
from core.module.module import Module

logging.basicConfig(level=logging.INFO)

modules: Dict[str, Module] = {
    # "UI": UIModule("UI"),
    "TextIndexer": TextIndexerModule("TextIndexer"),  # Used to index config data + each query
    # "TextToCommand": TextToCommandModule(),  # Recommend top N commands to execute according to query.
}

if __name__ == "__main__":
    controller = Controller(
        modules=modules
    )

    controller.setup()
