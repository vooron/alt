from collections import Callable
from typing import Dict

from controller.client import Event
from core.communication.topic import Topic
from core.module.impl.gui.module import UIModule
from core.module.module import Module
from core.subscription.impl.wake_up import wake_up_subscription

subscriptions: Dict[Topic, Callable[[Event], None]] = {
    Topic("core", "userFlow", "wakeUp"): wake_up_subscription
}

modules: Dict[str, Module] = {
    "UI": UIModule(),
    "TextToCommand": ...,
    "TextIndexer": ...,
}

if __name__ == "__main__":
    pass



"""
Event comes:
1) Create Event object and fill all fields (like source, etc.)
2) Check if event allowed.
3) Call function
"""



