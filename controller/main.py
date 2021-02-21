import asyncio
import threading
from typing import Any, Callable, Coroutine

import spacy
import websockets

from configs_main import apps_config_factory
from controller.server import ConnectionServer, Event
from text_to_command.configuration_units import SessionConfiguration, SystemConfiguration
from text_to_command.indexer import Indexer
from text_to_command.intent_resolver import IntentResolver

indexer = Indexer(spacy.load("en_core_web_md"))
intent_resolver = IntentResolver(indexer)


async def user_text_command_entered(event: Event, send_event: Callable[[Event], Coroutine[Any, Any, None]]):
    print("user_text_command_entered called")
    commands = intent_resolver.resolve_intent_recommendations(
        event.payload['user_text_command'],
        apps_config_factory(),
        SystemConfiguration([]), SessionConfiguration("", [])
    )

    payload = dict(
        items=[]
    )
    for c in sorted(commands, key=lambda x: x.score, reverse=True)[:5]:
        print(round(c.score, 3), " | ", c)
        payload['items'].append(dict(
            label=c.descriptive_name
        ))

    await send_event(Event("FrontEnd", "SHOW_COMMAND_VARIANTS", payload))


routes = {
    "USER_TEXT_COMMAND_ENTERED": user_text_command_entered
}

if __name__ == "__main__":
    server = ConnectionServer(routes)


    def start_server():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(server.on_websocket_connection, 'localhost', 4000)
        print("Server started!")
        loop.run_until_complete(start_server)
        loop.run_forever()


    t1 = threading.Thread(target=start_server)  # makes no sense.
    t1.start()
