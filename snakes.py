"""
Contains classes to simulate behaviour of snakes and world
Does NOT implement visualization or manual control of snakes, which must be handled outside this scope
"""
from __future__ import annotations
from typing import List
from random import randint

background_color = [0, 0, 0]
food_color = [0, 255, 0]

class Position:
    def __init__(self, x: int, y: int):
        self.x : int = x
        self.y : int = y
    
    def overlap(self, other: Position):
        return self.x == other.x and self.y == other.y
    
    def move(self, direction):
        if direction == 0:
            return Position(self.x, self.y - 1)
        elif direction == 1:
            return Position(self.x - 1, self.y)
        elif direction == 2:
            return Position(self.x, self.y + 1)
        elif direction == 3:
            return Position(self.x + 1, self.y)
        print(f"Error, cannot move in direction {direction}")
        return Position(self.x, self.y)
    
class WorldObject:
    def __init__(self, pos: Position, world: World, color: List[int], update_world = True):
        # Initial variables
        self.position: Position = pos
        self.world: World = world
        self.color: List[int] = color
        # Update world to hold object
        if update_world:
            world.set_tile(self)
        
    def kill(self):
        return

class Food(WorldObject):
    def __init__(self, pos, world, color):
        # This class for now only serves to mark an object as specifically food.
        # Future foods could be of different types, maybe to increment a snakes speed, make them shorter,
        # give them special abilities or provide aditional food.
        super().__init__(pos, world, color)
  
class World:
    def __init__(self, W: int, H: int):
        self.W = W
        self.H = H
        self.grid = [[WorldObject(Position(x, y), self, background_color, False) for y in range(H)] for x in range(W)]
    
    def get_tile_raw(self, x: int, y: int) -> WorldObject:
        return self.grid[x][y]
    
    def get_tile(self, pos: Position) -> WorldObject:
        return self.get_tile_raw(pos.x, pos.y)
        
    def remove_tile(self, wo: WorldObject):
        WorldObject(wo.position, self, background_color)
        wo.kill()

    def set_tile(self, wo: WorldObject, check_food = True):
        other = self.get_tile(wo.position)
        if check_food and isinstance(other, Food):
            self.respawn_food()
        self.grid[wo.position.x][wo.position.y] = wo
    
    def respawn_food(self):
        # Generate coords until an empty spot is found
        x = randint(0, self.W - 1)
        y = randint(0, self.H - 1)
        obj = self.get_tile_raw(x, y)
        while isinstance(obj, SnakePart) or isinstance(obj, Food):
            x = randint(0, self.W - 1)
            y = randint(0, self.H - 1)
        # The food itself handles updating the world grid to hold this by set_tile function
        Food(Position(x, y), self, food_color)
        
    def loop_pos(self, pos: Position) -> Position:
        return Position(pos.x % self.W, pos.y % self.H)

    def update_objs(self):
        for x in range(self.W):
            for y in range(self.H):
                wo = self.get_tile_raw(x, y)
                if isinstance(wo, SnakePart):
                    wo.life -= 1
                    if wo.life <= 0:
                        self.remove_tile(wo)

class SnakePart(WorldObject):
    def __init__(self, snake: Snake, pos: Position):
        self.snake = snake
        self.life = snake.length
        # Parent class handles holding the part in the world grid
        super().__init__(pos, snake.world, snake.color)
    
    def kill(self):
        self.snake.body.remove(self)

class Snake:
    def __init__(self, world: World, pos: Position, direction: int, length: int, color: List[int]):
        self.world: World = world
        self.head: Position = pos
        self.direction: int = direction
        self.last_dir: int = direction
        self.length: int = length
        self.color: List[int] = color
        self.body: List[SnakePart] = []
        self.alive: bool = True
        self.spawn_head()
        
    def spawn_head(self):
        # Don't need to handle part spawning because it itself does that on construction
        self.body.append(SnakePart(self, self.head))
    
    def move(self):
        self.head = self.world.loop_pos(self.head.move(self.direction))
        if isinstance(self.world.get_tile(self.head), SnakePart):
            self.alive = False
            return
        if isinstance(self.world.get_tile(self.head), Food):
            self.length += 1
        self.spawn_head()
        self.last_dir = self.direction
        
    def set_dir(self, dir: int):
        if dir == (self.last_dir + 2) % 4:
            return
        self.direction = dir

    def shorten(self):
        for bp in self.body:
            bp.life -= 1
            if bp.life == 0:
                self.world.remove_tile(bp)