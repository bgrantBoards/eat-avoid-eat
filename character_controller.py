"""
Hungry Sharks game controller
"""
import pygame, sys
from pygame.locals import *
from character import AIPlayer, Player
from hungry_sharks_field import HungrySharksField
from euclid3 import Vector2
from abc import ABC, abstractmethod

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
    
    @property
    def field(self):
        """
        A property which returns the Hungry Sharks Controller's private _field
        attribute.
        """
        return self._field
    
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
        # get mouse pos
        mouse_pos = pygame.mouse.get_pos()
        self._field.player.move_toward_point(mouse_pos, velocity_scaling=True, dt=1/self._fps)

class AIVelocityController(Controller):
    """
    Handles the control of every AI Player's movement and reaction behavior.

    Attributes:
        _fps (int): view fps (for movement control).
    """
    def __init__(self, field, fps=30):
        super().__init__(field)

        self._fps = fps
    
    def wander(self, aip):

        pass

    def attack(self, aip):
        aip.move_toward_point(self._field.player.position, dt=1/self._fps)
        pass

    def flee(self, aip):
        aip.move_away_from_point(self._field.player.position, dt=1/self._fps)
        pass
    
    behavior_switcher = {
        "wander": wander,
        "attack": attack,
        "flee": flee
    }

    def move(self):
        """
        Loops through every AI Player on the field and calls the movement
        functions that are appropriate to their behavior states.
        """
        for aip in self._field.characters:
            movement_function = self.behavior_switcher[aip.behavior_state]
            movement_function(self, aip)
    
