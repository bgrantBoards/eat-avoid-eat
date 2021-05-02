"""
Hungry Sharks playing field implementation.
"""
import math
from random import randrange
from euclid3 import Vector2
from character import Player, AIPlayer

def random_vector2(x_min, x_max, y_min, y_max):
    """
    Returns a Vector2 with random components within a specified range

    Args:
        x_min (float): x-component lower bound
        x_max (float): x-component upper bound
        y_min (float): y-component lower bound
        y_max (float): y-component upper bound

    Returns:
        Vector2: random Vector2
    """
    return Vector2(randrange(x_min, x_max), randrange(y_min, y_max))

class HungrySharksField():
    """
    Hungry Sharks playing field.

    Attributes:
        player: the player of the game
        characters: a list of AI characters currently in the game
        _max_nemeses: the maximum number of AI predators allowed on screen at a
        time

        To Do:
        ? _intensity
    """
    def __init__(self, window_x, window_y, num_characters):
        # window size parameters
        self.window_x = window_x
        self.window_y = window_y

        # create player 1
        self.player = Player(2, Vector2(window_x/2, window_y/2))

        # create AI players
        self.characters = []
        for _ in range(num_characters):
            self.spawn_new_ai(1)
        self._max_nemeses = 2

    @property
    def ai_players(self):
        """
        Returns private attribute _characters
        """
        return self.characters

    def check_collision(self, char1, char2):
        """
        Checks whether a pair of characters are colliding with one another.
        Returns True if they are and False otherwise.
        """
        distance = abs(char1.position - char2.position)
        r_greater = max(char1.size, char2.size)
        r_lesser = min(char1.size, char2.size)
        # return distance < r_greater - r_lesser + 2
        return distance < 30

    def player_collisions(self):
        """
        Returns any AIPlayers which the player is colliding with.

        Returns:
            list of players: who is being collided with. Empty list if no
            collisions.
        """
        collisions = []

        # check each AIPlayer against player1.
        # If they collide, add the AIPlayer to collisions
        for char in self.characters:
            if self.check_collision(self.player, char):
                collisions.append(char)

        return collisions

    def spawn_new_ai(self, size):
        """
        Adds a new AI player to the game at a random location.

        Args:
            size (int): size of the new player.
        """
        pos = random_vector2(0, self.window_x, 0, self.window_y)
        vel = random_vector2(5, 10, 5, 10)
        self.characters.append(AIPlayer(size, pos, vel, "wander"))
    
    def get_num_enemies(self):
        """
        Returns the number of AI players in the game larger than Player 1.
        """
        return sum([aip.size > self.player.size for aip in self.characters])

    def get_dist_to_walls(self, char):
        """
        Returns a list of distances from a character to the boundaries of the
        game's field.

        Args:
            char (Character): character to calculate wall distances for
        
        Returns:
            (list of floats): distances to walls in [lef, right, top, bottom]
            form
        """
        return [char.position.x,
                self.window_x - char.position.x,
                char.position.y,
                self.window_y - char.position.y]
    
    def get_closest_wall_direction(self, char):
        """
        Returns the "direction" of the closest wall to a character, a unit
        vector pointing parallel to that wall

        Args:
            char (Character): the character whose position is being considered
        """
        dist_to_walls = self.get_dist_to_walls(char)
        closest_wall_id = dist_to_walls.index(min(dist_to_walls))
        wall_cases = {0: Vector2(0, 1),
                      1: Vector2(0, 1),
                      2: Vector2(1, 0),
                      3: Vector2(1, 0)}
        return wall_cases[closest_wall_id]

    def update(self):
        """
        Takes care of player-to-player interations: collision detection,
        eating, growing, and respawn of AI players.
        """
        # Handle Player1 Eating AI players
        colliders = self.player_collisions()
        for aip in colliders:
            # grow the player
            growth_factor = 0.5 * aip.size / self.player.size * 100
            self.player.grow(growth_factor)
            # remove the collider
            self.ai_players.remove(aip)
            # spawn a new AI player that is smaller or one size bigger than player
            self.spawn_new_ai(randrange(1, self.player.size + 5))

        # update AI Player behavior states
        for aip in self.characters:
            # # avoid walls:
            # boundary_margin = 20
            # in_danger_zone = min(self.get_dist_to_walls(aip)) <= boundary_margin
            # if in_danger_zone:
            #     closest_wall_direction = self.get_closest_wall_direction(aip)
            #     if aip.will_collide_with_wall(closest_wall_direction):
            #         aip.behavior_state = "avoid walls"
            #         break

            # keep players in bounds
            boundary_margin = 20
            in_danger_zone = min(self.get_dist_to_walls(aip)) <= boundary_margin
            if in_danger_zone:
                aip.move

            # interact with player 1:
            dist_to_player = (aip.position - self.player.position).magnitude()
            if dist_to_player < aip.fov():
                # bigger AIs attack, smaller ones flee, and equal sized
                # ones keep wandering
                if aip.size > self.player.size:
                    aip.behavior_state = "attack"
                if aip.size < self.player.size:
                    aip.behavior_state = "flee"
            if dist_to_player > aip.fov():
                aip.behavior_state = "wander"
