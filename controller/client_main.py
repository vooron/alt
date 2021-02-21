import asyncio
import threading

from controller.client import ConnectionClient, Event


client = ConnectionClient("TestConsoleClient")


def on_event(event):
    print("Get:", event.target, event.payload)
    client.expose_event(event)


def init_client():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(on_event))
    loop.run_forever()


if __name__ == "__main__":

    t1 = threading.Thread(target=init_client)

    t1.start()

    while True:
        message = input("Enter message: ")

        if not message:
            exit()

        asyncio.run(client.expose_event(Event(target="CONTROLLER", action="INFO", payload=dict(
            message=message
        ))))


