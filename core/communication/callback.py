from dataclasses import dataclass

from core.communication.command_identifier import CommandIdentifier


@dataclass
class Callback:
    target: CommandIdentifier  # used to send answer back

    def to_dict(self):
        return {
            "target": str(self.target)
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            target=CommandIdentifier.deserialize(data['target'])
        )
