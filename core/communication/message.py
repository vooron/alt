import json
from dataclasses import dataclass, asdict
from typing import Optional, Dict

from core.communication.callback import Callback
from core.communication.command_identifier import CommandIdentifier
from core.communication.context_scope import ContextScope


@dataclass
class Message:
    payload: dict  # data transferred from 1 target to another
    target: CommandIdentifier  # unique action ID, to define subscription to process each event
    source: Optional[CommandIdentifier]  # used to define if action allowed
    context: Dict[ContextScope, dict]  # the data which will be persistent during the session in long message chain
    callback: Optional[Callback] = None  # triggered if successfully processed.

    def serialize(self):
        source = None
        if self.source:
            source = str(self.source)

        return json.dumps({
            "payload": self.payload,
            "source": source,
            "target": str(self.target),
            "context": {".".join(c): v for c, v in self.context.items()},
            "callback": self.callback.to_dict() if self.callback else None
        })

    @classmethod
    def deserialize(cls, message: str) -> 'Message':
        # TODO: add validations
        data = json.loads(message)
        return cls(
            payload=data['payload'],
            source=CommandIdentifier.deserialize(data['source']) if data.get('source') else None,
            target=CommandIdentifier.deserialize(data['target']),
            context={ContextScope(*source.split(".")): payload for source, payload in data['context'].items()},
            callback=Callback.from_dict(data['callback']) if data.get('callback') else None
        )
