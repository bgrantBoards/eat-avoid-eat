"""
Hungry Sharks game controller
"""
from abc import ABC, abstractmethod
import random
import math
import time
import pygame
from euclid3 import Vector2

def get_new_heading(curr_heading, degree_range):
    """
    Generate a random heading within a range of angles around the current
    heading

    Args:
        curr_heading (Vector2): the current heading
        degree_range (Vector2): angular width of slice around the current
            heading within which a new heading is chosen

    Returns:
        Vector2: new heading
    """
    rand_angle = random.uniform(-degree_range/2, degree_range/2)
    new_x = math.cos(rand_angle)*curr_heading.x - math.sin(rand_angle)*curr_heading.y
    new_y = math.sin(rand_angle)*curr_heading.x + math.cos(rand_angle)*curr_heading.y

    return Vector2(new_x, new_y)


class Controller(ABC):
    """
    Abstract base class for any child class which controls the input to a
    Hungry Sharks character.

    Attributes:
        _field: a private attribute which stores the game field in which
        controllable characters are stored.
        _view: the graphical interface of the game. The view is where user
        inputs come from.
    """
    def __init__(self, field):
        self._field = field

    @abstractmethod
    def move(self):
        """
        An abstract method for player control that will be overwritten in
        subclasses.
        """


class PlayerVelocityController(Controller):
    """
    Handles player input through mouse/keyboard inputs and controls the player's
    velocity and eating/growth behavior.

    Attributes:
        _fps (int): view fps (for movement control).
    """
    def __init__(self, field, fps=30):
        super().__init__(field)

        self._fps = fps

    def move(self):
        # move toward mouse
        mouse_pos = pygame.mouse.get_pos()
        self._field.player.move_toward_point(mouse_pos, velocity_scaling=False,\
            timestep=1/self._fps)

        # speed boosting
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self._field.player.boost = True
        else:
            self._field.player.boost = False

class AIVelocityController(Controller):
    """
    Handles the control of every AI Player's movement and reaction behavior.

    Attributes:
        _fps (int): view fps (for movement control).
    """
    def __init__(self, field, fps=30):
        super().__init__(field)

        self._fps = fps

    def avoid_walls(self, aip):
        """
        Velocity controller that steers an AI player away from window boundaries
        so that no player ever goes off-screen.

        Args:
            aip (AIPlayer): the AI Player that gets controlled.
        """
        # identify the direction of the wall to avoid
        dist_to_walls = self._field.get_dist_to_walls(aip)
        closest_wall_id = dist_to_walls.index(min(dist_to_walls))
        wall_cases = {0: Vector2(0, 1),
                      1: Vector2(0, 1),
                      2: Vector2(1, 0),
                      3: Vector2(1, 0)}
        wall_direction = wall_cases[closest_wall_id] # [1,0] or [0,1]

        # turn parallel to the wall to avoid going out of bounds
        # aip.move_parallel(wall_direction, timestep=1/self._fps)
        aip.bounce(wall_direction, timestep=1/self._fps)

    def wander(self, aip):
        """
        Defines AI wandering behavior
        """
        current_time = time.time()
        elapsed_time = current_time - aip.prev_tick

        aip.clock += elapsed_time

        if aip.clock > 0.2:
            degree_range = math.pi/6
            new_heading = get_new_heading(aip.velocity, degree_range)
            aip.velocity = new_heading
            aip.clock = 0
        else:
            aip.update_pos(1/self._fps)

        aip.prev_tick = current_time

    def attack(self, aip):
        """
        Defines AI attacking behavior
        """
        aip.move_toward_point(self._field.player.position, timestep=1/self._fps)

    def flee(self, aip):
        """
        Defines AI fleeing behavior
        """
        aip.move_away_from_point(self._field.player.position, timestep=1/self._fps)

    behavior_switcher = {
        "wander": wander,
        "attack": attack,
        "flee": flee,
        "avoid walls": avoid_walls
    }

    def move(self):
        """
        Loops through every AI Player on the field and calls the movement
        functions that are appropriate to their behavior states.
        """
        for aip in self._field.characters:
            movement_function = self.behavior_switcher[aip.behavior_state]
            movement_function(self, aip)
