import json
from dataclasses import dataclass
from json import JSONDecodeError
from typing import Callable, Union

import websockets
from websockets import WebSocketClientProtocol


@dataclass
class Event:
    target: str
    action: str
    payload: dict

    @classmethod
    def from_message(cls, message: Union[bytes, str]):
        data = json.loads(message)
        return Event(target=data['target'], action=data['action'], payload=data['payload'])

    def to_message(self):
        return json.dumps(dict(
            target=self.target,
            action=self.action,
            payload=self.payload
        ))


class ConnectionClient:
    source_id: str
    connection: WebSocketClientProtocol

    hostname: str = 'localhost'
    port: int = 4000

    def __init__(self, source_id: str):
        self.source_id = source_id

    async def authenticate(self, connection: WebSocketClientProtocol):
        await connection.send(Event(target='CONTROLLER', action="INIT_CONNECTION", payload=dict(
            source_id=self.source_id
        )).to_message())

    async def expose_event(self, event: Event):
        await self.connection.send(event.to_message())

    async def start(self, on_event: Callable[['ConnectionClient', Event], None]):
        async with websockets.connect(f"ws://{self.hostname}:{self.port}") as connection:
            await self.authenticate(connection)
            self.connection = connection
            async for message in connection:
                try:
                    event = Event.from_message(message)
                    on_event(self, event)
                except JSONDecodeError:
                    # TODO: handle
                    print("--JSON PARSE ERROR--")

