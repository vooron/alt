import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict

from core.communication.callback import Callback
from core.communication.command_identifier import CommandIdentifier


@dataclass
class Message:
    payload: dict  # data transferred from 1 target to another
    target: CommandIdentifier  # unique action ID, to define subscription to process each event
    source: Optional[CommandIdentifier]  # used to define if action allowed
    context: Dict[CommandIdentifier, dict]  # the data which will be persistent during the session in long message chain
    callback: Optional[Callback] = None  # triggered if successfully processed.

    def serialize(self):
        return json.dumps(asdict(self))

    @classmethod
    def deserialize(cls, message: str) -> 'Message':
        # TODO: add validations
        data = json.loads(message)
        return cls(
            payload=data['payload'],
            source=CommandIdentifier(*data['source']) if data.get('source') else None,
            target=CommandIdentifier(*data['target']),
            context={CommandIdentifier(*source): payload for source, payload in data['context'].items()},
            callback=Callback(**data['callback']) if data.get('callback') else None
        )






