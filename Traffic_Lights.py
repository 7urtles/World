from Cars import *

class Traffic_Light():
    def __init__(self):
        self.type = 'light'
        self.icon = '*'
        self.starting_timer = random.randint(0,1000)
        self.timer = self.starting_timer
        self.location = ''

    def create(world):
        if len(world.traffic_lights) < 2:
            for spawn in world.spawns:
                light = Traffic_Light()
                x,y = Car.convert(spawn)
                x = int(world.width // 2)
                location = Car.convert([x,y])
                world.spaces[location].layers[0] = light
                world.spaces[location].layers[0].location = location
                world.traffic_lights.append(light)
                # print(spawn)
        return world

    def light_changer(world):
        for light in world.traffic_lights:
            if light.timer == 0:
                world.spaces[light.location].layers[0] = False
                world.spaces[light.location].layers[1] = light
            elif light.timer == -light.starting_timer:
                world.spaces[light.location].layers[1] = False
                world.spaces[light.location].layers[0] = light
                light.timer = light.starting_timer
            light.timer -= 1
        return world