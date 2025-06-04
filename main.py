import pygame # For graphics
from random import randint # For random food spawns
from time import sleep
from snakes import *
pygame.init()

world = World(60, 40)
res = 20
display = pygame.display.set_mode([world.W*res, world.H*res])


def update_screen():
    for x in range(world.W):
        for y in range(world.H):
            obj = world.get_tile_raw(x, y)
            pygame.draw.rect(display, obj.color, pygame.Rect(x*res, y*res, res, res))
    pygame.display.flip()

# Spawn snake and food
p1 = Snake(world, Position(world.W//2, world.H//2 - 1), 0, 3, [200, 50, 0])
p2 = Snake(world, Position(world.W//2, world.H//2 + 1), 2, 3, [0, 50, 200])
world.respawn_food()
speed_decay = 0.999
speed = 0.20

def turn(event):
    if event.key == pygame.K_UP:
        p1.set_dir(0)
    elif event.key == pygame.K_LEFT:
        p1.set_dir(1)
    elif event.key == pygame.K_DOWN:
        p1.set_dir(2)
    elif event.key == pygame.K_RIGHT:
        p1.set_dir(3)
        
    if event.key == pygame.K_w:
        p2.set_dir(0)
    elif event.key == pygame.K_a:
        p2.set_dir(1)
    elif event.key == pygame.K_s:
        p2.set_dir(2)
    elif event.key == pygame.K_d:
        p2.set_dir(3)

def check_deaths():
    if p1.head.overlap(p2.head):
        return 3
    if not (p1.alive or p2.alive):
        return 3
    if not p2.alive:
        return 1
    if not p1.alive:
        return 2
    return 0

running = True
game_state = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            turn(event)
    
    if game_state == 0:
        world.update_objs()
        p1.move()
        p2.move()
        game_state = check_deaths()
        update_screen()
        
        sleep(speed)
        speed *= speed_decay
    else:
        if game_state == 1:
            while len(p2.body) > 0:
                p2.shorten()
                sleep(0.25)
                update_screen()
        elif game_state == 2:
            while len(p1.body) > 0:
                p1.shorten()
                sleep(0.25)
                update_screen()
        elif game_state == 3:
            while len(p1.body) > 0 or len(p2.body) > 0:
                p1.shorten()
                p2.shorten()
                sleep(0.25)
                update_screen()
        
        sleep(0.5)
        if game_state == 1:
            display.fill([200, 50, 0])
        elif game_state == 2:
            display.fill([0, 50, 200])
        elif game_state == 3:
            for x in range(world.W):
                for y in range(world.H):
                    pygame.draw.rect(display, [200, 50, 0] if (x+y)%2 else [0, 50, 200], pygame.Rect(x*res, y*res, res, res))
        pygame.display.flip()
        sleep(2)
        
        # Reset game
        world = World(world.W, world.H)
        p1 = Snake(world, Position(world.W//2, world.H//2 - 1), 0, 3, [200, 50, 0])
        p2 = Snake(world, Position(world.W//2, world.H//2 + 1), 2, 3, [0, 50, 200])
        world.respawn_food()
        speed_decay = 0.995
        speed = 0.50
        game_state = 0
                
        