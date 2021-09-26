import random

class Car:
    def __init__(self,id,location):
        self.id = id
        self.type = 'car'
        self.icon = '0'
        self.location = location
        self.old_location = ''
        self.direction = '1,0'
        self.next_location = location
        self.area = []
        self.wait = False

    def create(world):
        # Chance to spawn car
        chance = random.randint(40,50)
        if chance != 50:
            return world
        # If the spawn limit is not reached
        if len(world.cars) < world.max_cars:
            # Convert spawn dictonary to a list and pick a position from it
            location = random.choice(list(world.spawns))
            # If the chosen position is empty
            if world.spaces[location].layers[0] == False:
                # Build a new car
                car = Car(1,location)
                # Get movement vector from the spawn point
                car.direction = world.spawns[location]
                # Place it on the map
                world.spaces[location].layers[0] = car
                # Add it to the existing cars list
                world.cars.append(car)
            elif world.spaces[location].layers[0].type == 'spawn':
                # Build a new car
                car = Car(1,location)
                # Place it on the map
                world.spaces[location].layers[0] = car
                # Add it to the existing cars list
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
            # If wait is on skip movement for a frame
            if car.wait == True:
                car.wait = False
                continue
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
            try:
                # Remove the car from the old square
                world.spaces[old_location].layers[0] = False
                # Put it on the new location
                world.spaces[location].layers[0] = car
                # Remember where the car moved from
                car.old_location = old_location
            except:
                world.cars.pop(world.cars.index(car))
                pass
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
                # If the calculated space is not out of the map
                if x+newx < world.width and y+newy < world.height and x+newx >= 0 and y+newy >= 0:
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
        return world

    # Handling car behavior
    def decision_making(world):
        for car in world.cars:
            # Hold potential spaces to move to
            viable_moves = []
            # Go through movement options
            for possibility in car.area:
                # If that space is unoccupied
                if world.spaces[possibility].layers[0] == False:
                    # If the move is not backwards
                    if possibility != car.old_location and possibility != car.location:
                        viable_moves.append(possibility)
            # If space ahead is off the map, self destruct
            x,y = Car.convert(car.location)
            x1,y1 = Car.convert(car.direction)
            space_ahead = [x1+x,y1+y]
            space_ahead = Car.convert(space_ahead)
            try:
                world.spaces[space_ahead].layers[0]
            except:
                world.cars.pop(world.cars.index(car))
                world.spaces[car.location].layers[0] = False
                pass

            # If no viable moves, do not move
            if len(viable_moves) == 0:
                car.wait = True
                continue
            try:   
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
            except:
                pass