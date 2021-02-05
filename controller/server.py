import json
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from typing import Dict, Union

import asyncio
from websockets import WebSocketServerProtocol, ConnectionClosed


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


@dataclass
class Connection:
    source_id: str
    connection: WebSocketServerProtocol


class ConnectionServerException(Exception):
    code: int
    reason: str

    def __init__(self, code: int, reason: str):
        super(ConnectionServerException, self).__init__(reason)
        self.code = code
        self.reason = reason


class ConnectionServer:
    connections: Dict[str, Connection]

    def __init__(self):
        self.connections = {}

    async def on_connection_event(self, connection: Connection, event: Event):
        # TODO: logic
        print("Source:", connection.source_id, "| payload", event.payload)

    async def expose_event(self, event: Event):
        await self.connections[event.target].connection.send(event.to_message())

    def on_connection_close(self, connection: Connection):
        self.connections.pop(connection.source_id)
        print(f"Connection {connection.source_id} closed!")

    async def subscribe_to_connection_messages(self, connection: Connection):
        async for message in connection.connection:
            try:
                event = Event.from_message(message)
                await self.on_connection_event(connection, event)
            except JSONDecodeError:
                # TODO: handle
                print("--JSON PARSE ERROR--")

    async def register_websocket_connection(self, websocket: WebSocketServerProtocol) -> Connection:
        message = await websocket.recv()
        event = Event.from_message(message)
        if event.action != 'INIT_CONNECTION' or event.target != "CONTROLLER":
            raise ConnectionServerException(1007, reason="Connection init step missing.")
        connection = Connection(source_id=event.payload['source_id'], connection=websocket)
        self.connections[connection.source_id] = connection
        print(f"Connection with {connection.source_id} registered!")
        return connection

    async def on_websocket_connection(self, websocket: WebSocketServerProtocol, _: str) -> None:
        print("on_websocket_connection")
        try:
            connection = await self.register_websocket_connection(websocket)
            await self.subscribe_to_connection_messages(connection)
        except ConnectionServerException as e:
            await websocket.close(code=e.code, reason=e.reason)
        except ConnectionClosed:
            self.on_connection_close(connection) # noqa
