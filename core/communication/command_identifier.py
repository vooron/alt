from enum import Enum
from typing import NamedTuple


class ApplicationType(Enum):
    CORE = "CORE"
    MODULE = "MODULE"
    SKILL = "SKILL"


class CommandIdentifier(NamedTuple):
    type: ApplicationType
    application: str  # unique application id, like UI or TelegramClientBot.
    function: str  # application unique id: like switchOnTheLight
    command: str  # function unique id: like onAllParamsResolved
