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
        velocity: the character's current velocity
        speed: the character's maximum speed
    """
    def __init__(self, size = 1, position = Vector2(), velocity = Vector2(), speed=75):
        self._size = size
        self._position = position
        self.velocity = velocity
        self.speed = speed
    
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
    
    def move_toward_point(self, point, velocity_scaling=False, dt=1/30):
        # get displacement vector
        player_pos = self.position
        displacement = Vector2(point[0], point[1]) - player_pos
        distance = displacement.magnitude()

        # stop moving if on top of point
        if distance < 5:
            displacement = Vector2(0,0)
        
        # get the unit vector heading
        heading = displacement.normalize()
        
        # set the new velocity
        if velocity_scaling:
            v_scale = min(0.005*distance, 1)
        else:
            v_scale = 1
        self.velocity = heading * self.speed * v_scale

        # update position
        self.update_pos(dt)
    
    def move_away_from_point(self, point, dt=1/30):
        # get displacement vector
        player_pos = self.position
        displacement = Vector2(point[0], point[1]) - player_pos
        
        # get the unit vector heading away from the fleeing center
        heading = -1 * displacement.normalize()
        
        # set the new velocity
        self.velocity = heading * self.speed

        # update position
        self.update_pos(dt)
    

class Player(Character):
    """
    Hungry Sharks player.

    Inherits from Character.
    """
    def __init__(self, size = 2, position = Vector2(), velocity = Vector2(), speed = 75):
        """
        Create a new Player with default or custom parameters.
        """
        super().__init__(size, position, velocity, speed)
        self._growth_progress = 0

    def grow(self, factor = 10):
        print(factor)
        self._growth_progress += factor*10
        if self._growth_progress > 100:
            self._size += factor
            self._growth_progress = 0


class AIPlayer(Character):
    """
    Autonomous Hungry Sharks character.

    Inherits from Character.

    Attributes:
        _fov (int): radius at which the AI player can react to other players.
        behavior_state (string): defines how the AI controller moves the AI
            player.
    """
    def __init__(self, observation_radius, size = 2, position = Vector2(),\
        velocity = Vector2()):
        """
        Create a new AIPlayer with default or custom parameters.
        """
        super().__init__(size, position, velocity)

        self._fov = observation_radius
        self.behavior_state = "wander"
    
    @property
    def fov(self):
        return self._fov
