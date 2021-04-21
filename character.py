"""
A Hungry Sharks player or AI player.
"""
from euclid3 import Vector2

class Character():
    """
    An abstract base class for any class which generates a Hungry Sharks
    character.

    Attributes:
        _size: how big the character is
        _position: the character's current position
        _velocity: the character's current velocity
    """
    def __init__(self, size = 1, position = Vector2(), velocity = Vector2()):
        self._size = size
        self._position = position
        self.velocity = velocity
    
    @property
    def position(self):
        return self._position

    @property
    def size(self):
        return self._size
    
    def grow(self, factor = 10):
        self._size += factor
    
    def update_pos(self, dt):
        self._position += self.velocity * dt
    

class Player(Character):
    """
    Hungry Sharks player.

    Inherits from Character.
    """
    def __init__(self, size = 2, position = Vector2(), velocity = Vector2()):
        """
        Create a new Player with default or custom parameters.
        """
        super().__init__(size, position, velocity)


class AIPlayer(Character):
    """
    Autonomous Hungry Sharks character.

    Inherits from Character.
    """
    def __init__(self, observation_radius, size = 2, position = Vector2(),\
        velocity = Vector2()):
        """
        Create a new AIPlayer with default or custom parameters.
        """
        super().__init__(size, position, velocity)
        self._fov = observation_radius
    
    @property
    def fov(self):
        return self._fov
