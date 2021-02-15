#!/usr/bin/env python

import asyncio
import websockets


users = set()


async def notify_users(message):
    if users:
        await asyncio.wait([user.send(message) for user in users])


async def register_user(websocket):
    users.add(websocket)
    await notify_users(f'** Um usuário entrou na sala! **')


async def unregister_user(websocket):
    users.remove(websocket)
    await notify_users(f'** Um usuário saiu da sala! **')


async def server(websocket, path):
    await register_user(websocket)
    try:
        async for message in websocket:
            await notify_users(message)
    finally:
        await unregister_user(websocket)


start_server = websockets.serve(server, 'localhost', 6789)

asyncio.get_event_loop().run_until_complete(start_server)
print('Server Running...')
asyncio.get_event_loop().run_forever()
