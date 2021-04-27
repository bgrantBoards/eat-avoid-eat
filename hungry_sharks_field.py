"""
Hungry Sharks playing field implementation.
"""
from character import Player, AIPlayer
from random import randrange
from euclid3 import Vector2
import math

def random_Vector2(x_min, x_max, y_min, y_max):
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
        self.player = Player(size=20, position =\
            Vector2(window_x/2, window_y/2), speed=400)
        
        # created AI players
        self.characters = []
        for _ in range(num_characters):
            self.spawn_new_AI(10)
    
    
    @property
    def ai_players(self):
        return self.characters
    
    def check_collision(self, char1, char2):
        """
        Checks whether a pair of characters are colliding with one another.
        Returns True if they are and False otherwise.
        """
        distance = abs(char1.position - char2.position)
        r_greater = max(char1.size, char2.size)
        r_lesser = min(char1.size, char2.size)
        return distance < r_greater - r_lesser - 1

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
    
    def spawn_new_AI(self, size):
        """
        Adds a new AI player to the game at a random location.

        Args:
            size (int): size of the new player.
        """
        pos = random_Vector2(0, self.window_x, 0, self.window_y)
        vel = random_Vector2(5, 10, 5, 10)
        self.characters.append(AIPlayer(size = size, observation_radius=100,\
            position=pos, velocity=vel))
    
    def update(self):
        """
        Takes care of player-to-player interations: collision detection,
        eating, growing, and respawn of AI players.
        """
        # Handle Player1 Eating AI players
        colliders = self.player_collisions()
        for aip in colliders:
            # grow the player
            self.player.grow(aip.size/5)
            # remove the collider
            self.ai_players.remove(aip)
            # spawn a new AI player
            self.spawn_new_AI(randrange(10, math.floor(self.player.size) + 2))
        
        # update AI Player behavior states
        for aip in self.characters:
            dist_to_player = (aip.position - self.player.position).magnitude()
            if dist_to_player < aip.fov:
                aip.behavior_state = "flee"
            if dist_to_player > aip.fov:
                aip.behavior_state = "wander"

