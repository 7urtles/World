from Cars import *

class Road():
    def __init__(self,type,icon,spawn):
        self.type = type
        self.icon = icon
        self.spawn_location = spawn
        self.location = self.spawn_location

    def create(world):
        while world.roads < world.max_roads:
            # Generate random road spawning
            y = random.randint(5,world.height-7)
            spawn = Car.convert([0,y])
            Road.create_edges(world,spawn)
            Road.create_divider(world,spawn)
            Road.create_spawns(world,spawn)
            Road.create_barrier(world,spawn)
            world.roads += 1
        return world

    def create_edges(world,spawn):
        icon = '='
        type = 'edge'
        road = Road(type,icon,spawn)
        spawnx, spawny = Car.convert(road.spawn_location)
        # Scan all the map spaces for the spawn location
        for space in world.spaces:
        # Once it is found
            # Convert the locations into workable x,y coordinates
            x,y = Car.convert(space)
            # Check if the x-axis of the current piece is the same as the spawn x-axis
            if spawny == y or spawny == y -4:
            # Fill all the spaces along the x-axis with road pieces
                # Set the items location
                road.location = space
                # If so fill the piece with a road edge object
                world.spaces[space].layers[0] = road
        return world
    
    def create_divider(world,spawn):
        icon = '-'
        type = 'divider'
        road = Road(type,icon,spawn)
        spawnx, spawny = Car.convert(road.spawn_location)
        # Scan all the map spaces for the spawn location
        for space in world.spaces:
        # Once it is found
            # Convert the locations into workable x,y coordinates
            x,y = Car.convert(space)
            # Check if the x-axis of the current piece is the same as the spawn x-axis
            if spawny == y - 2:
            # Fill all the spaces along the x-axis with road pieces
                # Set the items location
                road.location = space
                # If so fill the piece with a road edge object
                world.spaces[space].layers[0] = road
        return world

    def create_barrier(world,spawn):
        icon = '7'
        type = 'barrier'
        road = Road(type,icon,spawn)
        spawnx, spawny = Car.convert(road.spawn_location)
        # Scan all the map spaces for the spawn location
        for space in world.spaces:
        # Once it is found
            # Convert the locations into workable x,y coordinates
            x,y = Car.convert(space)
            # Check if the x-axis of the current piece is the same as the spawn x-axis
            if spawny == y - 5:
            # Fill all the spaces along the x-axis with road pieces
                # Set the items location
                road.location = space
                # If so fill the piece with a road edge object
                world.spaces[space].layers[0] = road
        return world

    def create_spawns(world,spawn):
        icon = ' '
        type = 'spawn'
        road = Road(type,icon,spawn)
        spawnx, spawny = Car.convert(road.spawn_location)
        # Scan all the map spaces for the spawn location
        for space in world.spaces:
        # Once it is found
            # Convert the locations into workable x,y coordinates
            x,y = Car.convert(space)
            # Set spawns only on right side of roads
            if (x == spawnx and y == spawny+3) or (x == world.width-1 and y == spawny+1):
            # Fill all the spaces along the x-axis with road pieces
                # Set the items location
                road.location = space
                # If so fill the piece with a road edge object
                world.spaces[space].layers[0] = road
                if x < 1:
                    vector = '1,0'
                elif x > 1:
                    vector = '-1,0'
                world.spawns[space]=vector
            elif (x == spawnx and y == spawny+1) or (x == world.width-1 and y == spawny+3):
                world.spaces[space].layers[0] = False
        return world

    
