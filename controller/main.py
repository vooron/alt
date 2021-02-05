import asyncio
import threading

import websockets

from controller.server import ConnectionServer, Event

if __name__ == "__main__":
    server = ConnectionServer()

    def start_server():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        start_server = websockets.serve(server.on_websocket_connection, 'localhost', 4000)
        loop.run_until_complete(start_server)
        loop.run_forever()

    t1 = threading.Thread(target=start_server)
    t1.start()

    while True:
        action = input("Enter action: ")
        asyncio.run(server.expose_event(Event(target="FrontEnd", action=action, payload=dict())))
