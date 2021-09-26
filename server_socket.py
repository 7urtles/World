import asyncio
import websockets
import functools
import sys

from World import *
import time


async def hello(websocket, path, world):
    


    world = Car.create(world)
    world = Car.gather_area_information(world)
    Car.decision_making(world)
    world = Car.move_cars(world)
    world = Traffic_Light.create(world)
    world = Traffic_Light.light_changer(world)
    display_string = World.display(world)

    await websocket.send(display_string)
    
    time.sleep(world.run_speed)

async def main():
    world = World()
    world = Map_Square.create(world)
    world = Road.create(world)
    async with websockets.serve(functools.partial(hello, world=world), "localhost", 8700):
        await asyncio.Future()  # run forever

asyncio.run(main())