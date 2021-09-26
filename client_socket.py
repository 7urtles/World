import asyncio
import websockets
from os import system,name
from time import sleep
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')

async def hello():
    uri = "ws://localhost:8700"
    async with websockets.connect(uri) as websocket:
        greeting = await websocket.recv()
        print(f"{greeting}")
while True:
    try:
        asyncio.run(hello())
    except:
        print("Server Unreachable")
        print("Trying again in 5 seconds.....")
        sleep(5)
    # clear()


