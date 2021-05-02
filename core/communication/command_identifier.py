from enum import Enum
from typing import Union


class ApplicationType(Enum):
    CORE = "CORE"
    MODULE = "MODULE"
    SKILL = "SKILL"


class CommandIdentifier:
    type: ApplicationType
    application: str  # unique application id, like UI or TelegramClientBot.
    function: str  # application unique id: like switchOnTheLight
    command: str  # function unique id: like onAllParamsResolved

    def __init__(
            self,
            type: Union[str, ApplicationType],
            application: str,
            function: str,
            command: str
    ):
        if isinstance(type, str):
            self.type = ApplicationType[type]
        else:
            self.type = type

        self.application = application
        self.function = function
        self.command = command