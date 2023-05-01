import asyncio
import websockets

clients = []


async def send_message(message, sender):
    """
    Sends message to all the connected clients
    :param message:
    :param sender:

    """
    for client in clients:
        if client != sender:
            await client.send(message)


async def client_connected(websocket):
    """
    Called when the new client connects to the server
    :param websocket:
    """
    clients.append(websocket)
    try:
        async for message in websocket:
            """
            When message is received from the client , broadcast the message to all the clients
            """
            await send_message(message, websocket)
    finally:
        clients.remove(websocket)


async def start_server():
    """
    Starts the web server
    """
    async with websockets.serve(client_connected, "localhost", 8000):
        await asyncio.Future()  # Run Forever


if __name__ == '__main__':
    asyncio.run(start_server())
