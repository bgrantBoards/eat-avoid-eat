"""
Hungry Sharks game controller
"""
from pygame import mouse
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
    def __init__(self, field, view):
        self._field = field
        self._view
    
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

    """
    # get mouse pos
    # mouse_pos = pygame.mouse.get_pos()
    # print(mouse_pos)