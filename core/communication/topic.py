from typing import NamedTuple


class Topic(NamedTuple):
    entity_type: str  # one of allowed. For example: Module, Skill
    entity_id: str  # name of entity, like UI, or TelegramClientBot.
    id: str
