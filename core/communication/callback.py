from dataclasses import dataclass

from core.communication.command_identifier import CommandIdentifier


@dataclass
class Callback:
    target: CommandIdentifier  # used to send answer back
