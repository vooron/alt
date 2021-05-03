from enum import Enum
from typing import Union, Optional


class ApplicationType(Enum):
    CORE = "CORE"
    MODULE = "MODULE"
    SKILL = "SKILL"


class CommandIdentifier:
    type: ApplicationType
    application: str  # unique application id, like UI or TelegramClientBot.
    function: Optional[str] # application unique id: like switchOnTheLight
    command: Optional[str] # function unique id: like onAllParamsResolved

    SEPARATOR = "."

    def __init__(
            self,
            type: Union[str, ApplicationType],
            application: str,
            function: Optional[str] = None,
            command: Optional[str] = None
    ):
        if isinstance(type, str):
            self.type = ApplicationType[type]
        else:
            self.type = type

        self.application = application
        self.function = function
        self.command = command

    def __str__(self):
        parts = [self.type.name, self.application]
        if self.function:
            parts.append(self.function)
            if self.command:
                parts.append(self.command)
        return self.SEPARATOR.join(parts)

    @classmethod
    def deserialize(cls, data: str) -> 'CommandIdentifier':
        parts = data.split(cls.SEPARATOR)

        return cls(*parts)
