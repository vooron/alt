import logging
from typing import Dict

from core.communication.connection_service import ConnectionService
from core.communication.message import Message
from core.module.module import Module


class Controller:
    _modules: Dict[str, Module]
    _connection_service: ConnectionService

    def __init__(self, modules: Dict[str, Module]):
        self._modules = modules
        self._connection_service = ConnectionService(self.on_event)

    def on_event(self, event: Message):
        """check access permissions, translate event to target or handler"""
        print(event.payload)
        #
        # with open("test_index_data.json", 'w') as f:
        #     json.dump(event.payload, f)

    def _setup_modules(self):
        logging.info("=== Init modules start ===")
        for module_name, module in self._modules.items():
            module.setup(self._connection_service)
            logging.info(f"Module {module_name} inited.")
        logging.info("=== Init modules end ===")

    def setup(self) -> None:
        self._setup_modules()

        # self._connection_service.dispatch(Message(
        #     source=None,
        #     target=CommandIdentifier(ApplicationType.MODULE, "TextIndexer", "indexation", "get_indexed_data"),
        #     context={},
        #     callback=Callback(target=CommandIdentifier(ApplicationType.CORE, "app", "function", "command")),
        #     payload={
        #         "telegram": {
        #             "type": "SKILL",
        #             "name": "Telegram",
        #             "description": "Telegram Client bot for integrations with locally installed Telegram application.",
        #             "tags": ["Telegram", "Messenger", "Messages", "Communication"]
        #         },
        #         "telegram.unread_messages": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "List unread messages",
        #             "description": "List all new messages from Telegram.",
        #             "call_examples": [
        #                 "Read messages",
        #                 "Is there new messages",
        #                 "Anything new",
        #                 "Unread messages",
        #                 "Messages",
        #                 "Any messages"
        #             ]
        #         },
        #         "telegram.send_message": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "Send message",
        #             "description": "Send messenger with Telegram client with active account.",
        #             "call_examples": ["Send message", "Send", "Write", "Write message"]
        #         },
        #
        #         "email": {
        #             "type": "SKILL",
        #             "name": "EMail",
        #             "description": "Email integration for managing emaild from GMail.",
        #             "tags": ["Mail", "GMail", "Email", "Communication"]
        #         },
        #         "email.unread_mails": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "List unread mail",
        #             "description": "Lists all new mail from GMail.",
        #             "call_examples": [
        #                 "Read mail",
        #                 "Read email",
        #                 "Are there new mails",
        #                 "Anything new",
        #                 "Unread mail",
        #                 "Unread email",
        #                 "Any mail"
        #             ]
        #         },
        #         "email.send_mail": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "Send mail",
        #             "description": "Sends mail with your GMail account.",
        #             "call_examples": ["Send mail", "Send", "Write", "Write mail"]
        #         },
        #
        #         "timer": {
        #             "type": "SKILL",
        #             "name": "Timer",
        #             "description": "Timer",
        #             "tags": ["Timer", "Time management"]
        #         },
        #         "timer.start_new": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "Start timer",
        #             "description": "Starts timer for specified time.",
        #             "call_examples": ["Remind me in", "Call me in", "Start timer for", "Set timer for"]
        #         },
        #         "timer.disable_all": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "Disable all timers",
        #             "description": "Disables all active timers",
        #             "call_examples": ["Suppress all", "Disable all"]
        #         },
        #         "timer.list": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "List active timers",
        #             "description": "Lists all active timers",
        #             "call_examples": ["List all", "Show all"]
        #         },
        #
        #         "calendar": {
        #             "type": "SKILL",
        #             "name": "Calendar",
        #             "description": "Google calendar management",
        #             "tags": ["Calendar", "Google Calendar"]
        #         },
        #         "calendar.list": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "List events",
        #             "description": "Shows all events for specified date",
        #             "call_examples": ["List events", "Whats for", "Any events for"]
        #         },
        #
        #         "stopwatch": {
        #             "type": "SKILL",
        #             "name": "Stopwatch",
        #             "description": "Google calendar management",
        #             "tags": ["Stopwatch", "Time management"]
        #         },
        #         "stopwatch.start_new": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "Start stopwatch",
        #             "description": "Starts stopwatch",
        #             "call_examples": ["Start stopwatch", "Launch stopwatch"]
        #         },
        #
        #         "alarm_clock": {
        #             "type": "SKILL",
        #             "name": "Alarm clock",
        #             "description": "Alarm clock",
        #             "tags": ["Alarm clock"]
        #         },
        #         "alarm_clock.start_new": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "Start alarm clock",
        #             "description": "Starts alarm clock for specified date and time",
        #             "call_examples": ["Start alarm for", "Launch alarm for", "Create alarm for"]
        #         },
        #         "alarm_clock.list": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "List active alarms",
        #             "description": "Lists active alarm clocks",
        #             "call_examples": ["List alarms"]
        #         },
        #         "alarm_clock.show_nearest": {
        #             "type": "SKILL_FUNCTION",
        #             "name": "Show nearest alarm",
        #             "description": "Show nearest active alarm clock",
        #             "call_examples": ["Show nearest alarm", "Show next alarm"]
        #         },
        #     }
        # ))
