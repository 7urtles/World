from Traffic_Lights import *
from time import sleep
from Cars import *
from Roads import *
from os import system,name
#    [-----WORLD-----]
# One WORLD to contain them all
class World:
    # Initial world settings
    def __init__(self):
        self.name = 'Charles'
        self.size = 50
        self.height = self.size
        self.width = self.size*4
        self.max_cars = 500
        self.max_roads = 3
        self.run_speed = .00
        self.cars = []
        self.roads = 0
        self.traffic_lights = []
        self.spaces = {}
        self.spawns = {}
        self.updated_squares = []
    
    # Start the environment
    def run():
        world = World()
        world = Map_Square.create(world)
        world = Road.create(world)
        while True:
            world = Car.create(world)
            world = Car.gather_area_information(world)
            Car.decision_making(world)
            world = Car.move_cars(world)
            world = Traffic_Light.create(world)
            world = Traffic_Light.light_changer(world)
            World.display(world)
            sleep(world.run_speed)
    
    # Renders the world to the console
    def display(world):
        display_string = ''
        x=0
        y=0
        while y < world.height:
            location = Car.convert([x,y])
            if world.spaces[location].layers[0] != False:
                display_string += world.spaces[location].layers[0].icon
            else:
                display_string += ' '
            x += 1
            if x == world.width:
                display_string += '\n'
                x = 0
                y+=1
        print(display_string)


#    [-----SPACES-----]
# These are the spaces that make up the map
class Map_Square():
    # Gets id from create()
    def __init__(self,id):
        self.id = id
        self.icon = '-'
        self.layers = {}
        # Build the z-axis layers
        for layer in range(20,0,-1):
            self.layers[layer] = {}
        self.layers[0] = False
    # Create world spaces from world.size
    def create(world):
        x=0
        y=0
        while y < world.height: 
            if x == world.width:
                x = 0
                y += 1
            position = Car.convert([x,y])
            square = Map_Square(position)
            if y == world.height:
                break
            if y == 0 or x == 0 or y == world.height-1 or x == world.width-1:
                square.layers[0] = Edge()
            world.spaces[position]=square
            x+=1
        return world    

class Edge:
    # Initial world settings
    def __init__(self):
        self.icon = '*'
        self.type = 'edge'

# clear screen
def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
World.run()