"""
Hungry Sharks playing field implementation.
"""
from character import Player, AIPlayer
from random import randrange
from euclid3 import Vector2

def random_Vector2(x_min, x_max, y_min, y_max):
    return Vector2(randrange(x_min, x_max), randrange(y_min, y_max))

class HungrySharksField():
    """
    Hungry Sharks playing field.

    Attributes:
        _player: the player of the game
        _characters: a list of AI characters currently in the game

        To Do:
        ? _intensity
    """
    def __init__(self, window_x, window_y, num_characters):
        self.window_x = window_x
        self.window_y = window_y
        self._player = Player(size=20, position =\
            Vector2(window_x/2, window_y/2))
        self._characters = []
        for _ in range(num_characters):
            pos = random_Vector2(0, window_x, 0, window_y)
            vel = random_Vector2(5, 10, 5, 10)
            self._characters.append(AIPlayer(size = 10, observation_radius=100,\
                position=pos, velocity=vel))
    
    @property
    def player(self):
        return self._player
    
    @property
    def ai_players(self):
        return self._characters
    
    def check_collision(self, char1, char2):
        """
        Checks whether a pair of characters are colliding with one another.
        Returns True if they are and False otherwise.
        """
        distance = abs(char1.pos - char2.pos)
        return distance - char1.size - char2.size < 0

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
        for char in self._characters:
            if self.check_collision(self._player, char):
                collisions.append(char)
        
        return collisions
