from dataclasses import dataclass

from core.communication.topic import Topic


@dataclass
class Callback:
    topic: Topic  # used to send answer back