"""
Hungry Sharks playing field implementation.
"""
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

def check_collision(char1, char2):
    """
    Checks whether a pair of characters are colliding with one another.
    Returns True if they are and False otherwise.
    """
    distance = abs(char1.position - char2.position)
    return distance < 30

class HungrySharksField():
    """
    Hungry Sharks playing field.

    Attributes:
        player: the player of the game
        characters: a list of AI characters currently in the game
        _max_nemeses: the maximum number of AI predators allowed on screen at a
        time
        game_end: a string that is empty as long as the player has not won
        or lost the game and is "win" or "lose" when the game ends
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
            new_aip = self.get_new_ai(1)
            self.spawn_new_ai(new_aip)
        self._max_nemeses = 2
        self.game_end = ""

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
            if check_collision(self.player, char):
                collisions.append(char)

        return collisions

    def get_new_ai(self, size):
        """
        Returns a new AI player with a random location.

        Args:
            size (int): size of the new player.
        """
        pos = random_vector2(50, self.window_x - 50, 50, self.window_y - 50)
        vel = Vector2(0,0)
        aip = AIPlayer(size, pos, vel, "wander")
        aip.velocity = random_vector2(-10, 10, -10, 10).normalize() * aip.max_speed()
        return aip

    def spawn_new_ai(self, aip):
        """
        Add an AI character to the game.

        Args:
            aip (AIPlayer): the aip to be spawned in.
        """
        self.characters.append(aip)

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

    def update_ai_behaviors(self):
        """
        Checks the state of the field and updates ai players to behave correctly
        """
        for aip in self.characters:
            # avoid walls:
            boundary_margin = 25
            in_danger_zone = min(self.get_dist_to_walls(aip)) <= boundary_margin
            if in_danger_zone:
                closest_wall_direction = self.get_closest_wall_direction(aip)
                if aip.will_collide_with_wall(closest_wall_direction):
                    aip.behavior_state = "avoid walls"
                continue

            # interact with player 1:
            dist_to_player = (aip.position - self.player.position).magnitude()
            if dist_to_player < aip.fov():
                # bigger AIs attack, smaller ones flee, and equal sized
                # ones keep wandering
                if aip.size > self.player.size:
                    aip.behavior_state = "attack"
                if aip.size < self.player.size:
                    aip.behavior_state = "flee"
            else:
                aip.behavior_state = "wander"

    def handle_eating_and_win_lose(self):
        """
        Checks state of the field and updates players when an eating event
        occurs.
        """
        # Handle Player1 Eating AI players and winning/losing the game
        colliders = self.player_collisions()
        for aip in colliders:
            # determine if the player won or lost the match:
            if aip.size > self.player.size:
                # Player loses the game!
                self.game_end = "lose"
            elif aip.size < self.player.size:
                # grow the player
                growth_factor = 0.5 * aip.size / self.player.size * 100
                self.player.grow(growth_factor)
                # remove the collider
                self.characters.remove(aip)
                # spawn a new AI player that is smaller or one size bigger than player
                if self.get_num_enemies() < 2:
                    new_aip = self.get_new_ai(randrange(\
                        max(1, self.player.size - 2),\
                        min(self.player.size + 3, 10)))
                else:
                    new_aip = self.get_new_ai(randrange(\
                        max(1, self.player.size - 2),\
                        self.player.size))
                new_aip.relocate(self.player, self.window_x, self.window_y)
                self.spawn_new_ai(new_aip)
            if self.player.size > 10:
                self.game_end = "win"

    def update(self):
        """
        Takes care of player-to-player interations: collision detection,
        eating, growing, and respawn of AI players.
        """
        self.update_ai_behaviors()
        self.handle_eating_and_win_lose()
