from hashlib import new
from time import process_time_ns, sleep
import random
#    [-----WORLD-----]
# One WORLD to contain them all
class World:
    # Initial world settings
    def __init__(self):
        self.name = 'Charles'
        self.size = 120
        self.height = self.size
        self.width = self.size*5.1
        self.max_cars = 5000
        self.run_speed = .00
        self.cars = []
        self.spaces = {}
        self.updated_squares = []
    
    # Start the environment
    def run():
        world = World()
        world = Map_Square.create(world)
        while True:
            world = Car.create(world)
            world = Car.move_cars(world)
            World.display(world)
            # sleep(world.run_speed)
    
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
class Car:
    def __init__(self,id,location):
        self.id = id
        self.type = 'car'
        self.icon = '0'
        self.location = location
        self.direction = '1,1'
        self.next_location = location
        self.area = []
    def create(world):
        print(len(world.cars))
        x = random.randint(0,world.width-5)
        y = random.randint(0,world.height-5)
        location = str(x)+','+str(y)
        while len(world.cars) < world.max_cars and world.spaces[location].layers[0] == False:
            car = Car(1,location)
            world.spaces[location].layers[0] = car
            world.cars.append(car)
        return world
    # Does conversion from a coordinate in string form to a coordinate in list form, and vice versa
    def convert(location):
        if type(location) == str:
            x = int(location[0:location.index(',')])
            y = int(location[location.index(',')+1:])
            return x,y
        else:
            location = str(location[0])+','+str(location[1])
            return location
    # Updates car location
    def move_cars(world):
        for car in world.cars:
            # Find where the car is 
            old_location = car.location
            # Covert location to grid square
            x,y = Car.convert(old_location)
            # Convert cars movement direction to gird vector
            x1,y1 = Car.convert(car.direction)
            # Calculate it's new location
            location = Car.convert([x+x1,y+y1])
            # Adjust the cars location stat
            car.location = location
            # Remove the car from the old square
            world.spaces[old_location].layers[0] = False
            # Put it on the new location
            world.spaces[location].layers[0] = car
            # Add the updated squares to a list to help with rendering processing power
            # world.updated_squares.append(world.spaces[old_location].id)
            # world.updated_squares.append(world.spaces[location].id)
        world = Car.gather_area_information(world)
        return world

    def gather_area_information(world):
        # Scan throught the cars
        for car in world.cars:
            # Convert location to workable integers
            x,y = Car.convert(car.location)
            newx = -1
            newy = -1
            locations = []
            # Cycle through each space withing 1 grid square of the car
            while newy <= 1:
                locations.append([x+newx,y+newy])
                newx += 1
                if newx > 1:
                    newx = -1
                    newy += 1
            # Clear previous area data
            car.area = []
            # Convert new location back to a string, and add them to the cars area list
            for location in locations:
                location =  Car.convert(location)
                car.area.append(location)
        Car.decision_making(world)
        return world

    # Handling car behavior
    def decision_making(world):
        for car in world.cars:
            viable_moves = []
            # Go through movement options
            for possibility in car.area:
                # If that space is unoccupied
                if world.spaces[possibility].layers[0] == False:
                    viable_moves.append(possibility)
                
            # Randomly pick a move
            choice = random.choice(viable_moves)
            # Calculate movement vector to that location
            x,y = Car.convert(car.location)
            x1,y1 = Car.convert(choice)
            vector = [x1-x,y1-y]
            # Convert the vector back to a string
            vector = Car.convert(vector)
            # Make the cars movement direction the new vector
            car.direction = vector

World.run()