import pygame, sys
from pygame.locals import *
import random
from World import *
from Cars import *
from Roads import *
from Traffic_Lights import *

pygame.init()

# clock for fps counter
clock = pygame.time.Clock()

# Window title
pygame.display.set_caption('World')

# Window size
window_size = (1000,1000)

# Build screen
screen = pygame.display.set_mode(window_size,0,32)

# Display size??
display = pygame.Surface((500,500))

# Player Image
player_image = pygame.image.load('assets/Character with sword and shield/idle/idle right1.png')

# Tree Image
tree_image = pygame.image.load('assets/spritesheet/props_tree.png')

# Chest Image
chest_image = pygame.image.load('assets/spritesheet/props_chest_closed.png')

# Map for game
game_map = []
for x in range(0,10):
    row = []
    for y in range(0,10):
        row.append(random.randint(0,3))
    game_map.append(row)

world = World()
game_map = Map_Square.create(world)
world = Road.create(world)

moving_right = False
moving_left = False
moving_up = False
moving_down = False

# Initial player location
player_location = [50,display.get_height()-player_image.get_height()]
player_y_momentum = 0

# Player collission rectangle
player_rect = pygame.Rect(player_location[0],player_location[1],player_image.get_width(),player_image.get_height())

# Game loop
while True:
    # Updating and moving cars
    world = Car.create(world)
    world = Car.gather_area_information(world)
    Car.decision_making(world)
    world = Car.move_cars(world)
    world = Traffic_Light.create(world)
    world = Traffic_Light.light_changer(world)

    # Clear the screen by filling with a color
    display.fill((255,255,255))

    # Render map tiles
    # for space in world.spaces:
    #     x,y = Car.convert(space)
    #     display.blit(tree_image,(x*16, y*16))
    for car in world.cars:
        x,y = Car.convert(car.location)
        display.blit(chest_image,(x*16, y*16))

    # Stacks the player image on the screen
    display.blit(player_image,player_location)

    player_y_momentum += 0
    player_location[1] += player_y_momentum

    # Move player
    if moving_right == True:
        player_location[0] += 4
    if moving_left == True:
        player_location[0] -= 4
    if moving_up == True:
        player_location[1] -= 4
    if moving_down == True:
        player_location[1] += 4

    # Update player collision rectangle
    player_rect.x = player_location[0]
    player_rect.y = player_location[1]

    # Check for a quit event within the game events
    for event in pygame.event.get():
        if event.type == QUIT:
            print('Quitting game')
            pygame.quit()
            sys.exit()
            

        # Check for key press
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                player_image = pygame.image.load('assets/Character with sword and shield/idle/idle right1.png')
                moving_right = True
            if event.key == K_LEFT:
                player_image = pygame.image.load('assets/Character with sword and shield/idle/idle left1.png')
                moving_left = True
            if event.key == K_UP:
                player_image = pygame.image.load('assets/Character with sword and shield/idle/idle up1.png')
                moving_up = True
            if event.key == K_DOWN:
                player_image = pygame.image.load('assets/Character with sword and shield/idle/idle down1.png')
                moving_down = True

        # Check for key release
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False
            if event.key == K_UP:
                moving_up = False
            if event.key == K_DOWN:
                moving_down = False

    # Image scaling?
    surf = pygame.transform.scale(display, window_size)
    screen.blit(surf, (0,0))
    # Refreshes the screen
    pygame.display.update()
    clock.tick(60)