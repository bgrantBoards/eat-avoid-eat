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
        _growth_progress: percentage toward evolution
        velocity: the character's current velocity
    """
    def __init__(self, size, position):
        self._size = size
        self._position = position
        self._growth_progress = 0
        self.velocity = Vector2(0, 0)

    @property
    def position(self):
        """
        Returns private attribute _position
        """
        return self._position

    @property
    def size(self):
        """
        Returns private attribute _size
        """
        return self._size

    @property
    def growth_progress(self):
        """
        Returns private attribute _growth_progress
        """
        return self._growth_progress

    speed_from_size = {
        1: 50,
        2: 75,
        3: 70,
        4: 68,
        5: 65,
        6: 65,
        7: 60,
        8: 58,
        9: 55,
        10: 50
    }

    def max_speed(self):
        """
        Returns a character's maximum speed based on its size.

        Returns:
            [float]: Character's max speed
        """
        max_speed_scale = 2
        return self.speed_from_size[self.size] * max_speed_scale

    def grow(self, factor):
        """
        adjusts character's growth progress up and evolves the character if
        growth_progress is above 100.
        """
        self._growth_progress += factor

        if self._growth_progress > 100:
            self._growth_progress = 15
            self._size += 1

    def update_pos(self, timestep):
        """
        Moves character's position based on velocity.

        Arguments:
            timestep: duration of the timestep over which the positional update
            happens
        """
        self._position += self.velocity * timestep

    def move_toward_point(self, point, velocity_scaling=False, timestep=1/30):
        """
        Changes the Character's velocity to point toward a point.

        Args:
            point (Vector2): target point
            velocity_scaling (bool, optional): determines whether the magnitude
            of the Character's velocity is scaled down the closer it gets to the
            target point. Defaults to False.
            timestep (float, optional): timestep (1/frame rate). Defaults to 1/30.
        """
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
        self.velocity = heading * self.max_speed() * v_scale

        # update position
        self.update_pos(timestep)

    def move_away_from_point(self, point, timestep=1/30):
        """
        Changes the Character's velocity to point away from a point.

        Args:
            point (Vector2): center of the fleeing movement.
            timestep (float, optional): timestep (1/frame rate). Defaults to 1/30.
        """
        # get displacement vector
        player_pos = self.position
        displacement = Vector2(point[0], point[1]) - player_pos

        # get the unit vector heading away from the fleeing center
        heading = -1 * displacement.normalize()

        # set the new velocity
        self.velocity = heading * self.max_speed()

        # update position
        self.update_pos(timestep)

    def move_parallel(self, direction, timestep=1/30):
        """
        Update velocity to move parallel with a direction vector.

        Args:
            (Vector2) direction: the direction vector to move parallel with
        """
        move_backwards = direction.dot(self.velocity) < 0
        if move_backwards:
            new_v = direction.normalize() * self.max_speed() * -1
        else:
            new_v = direction.normalize() * self.max_speed()
        self.velocity = new_v

        # move
        self.update_pos(timestep)

    def bounce(self, wall_direction, timestep=1/30):
        """
        Reflects character's velocity to bounce off of a wall.

        Args:
            wall_direction (Vector2): defines the orientation of the wall.
            timestep (float): timestep (1/frame rate). Defaults to 1/30.
        """
        self.velocity = self.velocity.reflect(Vector2(wall_direction.y, wall_direction.x))
        self.update_pos(timestep)

        # self.velocity = self.velocity.reflect(wall_direction)

    def will_collide_with_wall(self, wall_direction):
        """
        Returns True if the character is on a trajectory to hit a specific wall.
        Returns False otherwise.

        Args:
            wall_direction (Vector2): a vector parallel to the wall you want to
            check

        Returns:
            bool
        """
        # return self.velocity.angle(wall_direction) < 0 # cross product
        return (self.velocity.x*wall_direction.y) - (self.velocity.y*wall_direction.x)


class Player(Character):
    """
    Hungry Sharks player.

    Inherits from Character.

    Attributes:
        boost (bool): determines whether the player is currently boosting.
    """
    def __init__(self, size, position):
        """
        Create a new AIPlayer with default or custom parameters.
        """
        super().__init__(size, position)
        self.boost = False

    def max_speed(self):
        """
        Returns the player's boosted or un-boosted max speed.

        Returns:
            [float]: Character's max speed
        """
        max_speed_scale = 2
        boost_scale = 1
        if self.boost & (self.growth_progress > 0):
            boost_scale = (1.5*self.boost)

        return self.speed_from_size[self.size] * max_speed_scale * boost_scale

    def update_pos(self, timestep):
        """
        Moves character's position based on velocity. Also decreases growth
        progress when boosting

        Arguments:
            timestep: duration of the timestep over which the positional update
            happens
        """
        growth_decay_rate = 15 # growth progress points / second
        if self.boost:
            self._growth_progress -= growth_decay_rate * timestep
        self._position += self.velocity * timestep


class AIPlayer(Character):
    """
    Autonomous Hungry Sharks character.

    Inherits from Character.

    Attributes:
        _fov (int): radius at which the AI player can react to other players.
        behavior_state (string): defines how the AI controller moves the AI
            player.
        clock: keeps track of time for random motion switching
        prev_tick: keeps track of the previous system time
    """
    def __init__(self, size, position, velocity, behavior_state):
        """
        Create a new AIPlayer with default or custom parameters.
        """
        super().__init__(size, position)
        self.velocity = velocity
        self.behavior_state = behavior_state
        self.clock = 0
        self.prev_tick = 0


    fov_from_size = {
        1: 50,
        2: 75,
        3: 70,
        4: 68,
        5: 65,
        6: 65,
        7: 60,
        8: 58,
        9: 55,
        10: 50
    }

    def fov(self):
        """
        Returns an AI player's field of view (reaction radius).

        Returns:
            [float]: Character's FOV
        """
        scale_factor = 3
        return self.fov_from_size[self.size] * scale_factor

    def relocate(self, player, window_x, window_y):
        """
        Move the AI Player away from player (safely).

        Args:
            player (Player): player
        """
        player_to_aip = self.position - player.position

        if player_to_aip.magnitude() < self.fov() + 50:
            window_center = Vector2(window_x/2, window_y/2)
            player_to_window_center = window_center - player.position

            safe_pos = player.position + player_to_window_center.normalize() * self.fov() * 1.25
            self._position = safe_pos
