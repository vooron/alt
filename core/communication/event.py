import json
from dataclasses import dataclass, asdict
from typing import Optional

from core.communication.callback import Callback
from core.communication.topic import Topic


@dataclass
class Event:
    payload: dict
    source: Optional[str]  # used to define if action allowed
    topic: Topic  # unique action ID, to define subscription to process each event
    session_id: Optional[str]  # unique identifier of the session
    callback: Optional[Callback]

    def serialize(self):
        return json.dumps(asdict(self))

    @classmethod
    def deserialize(cls, message: str) -> 'Event':
        # TODO: add validations
        data = json.loads(message)
        return cls(
            payload=data['paylaod'],
            source=data.get('source'),
            topic=Topic(*data['topic']),
            session_id=data.get('session_id'),
            callback=Callback(**data['callback']) if data.get('callback') else None
        )
