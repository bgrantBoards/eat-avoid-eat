"""
Hungry Sharks game view
"""
from abc import ABC, abstractmethod
import sys
from colorsys import hsv_to_rgb
import pygame
from pygame.locals import QUIT


def hsv2rgb(h,s,v):
    return tuple(round(i * 255) for i in hsv_to_rgb(h,s,v))


class HungrySharksView(ABC):
    """
    An abstract base class for any class which generates a view of the
    Hungry Sharks game.

    Attributes:
        _field: a private attribute which stores the game field to be viewed
    """
    def __init__(self, field):
        """
        Sets the ABC's _field attribute

        Args:
            field: Hungry Sharks game field representation
        """
        self._field = field

    @property
    def field(self):
        """
        Returns private attribute _field
        """
        return self._field

    @abstractmethod
    def draw(self):
        """
        An abstract method for player view that will be overwritten in
        subclasses.
        """


class PyGameView(HungrySharksView):
    """
    A viewing class for graphics using PyGame.

    Inherits from HungrySharksView

    Attributes:
        _field: stores the game field
        _window: a pygame window used to draw on
        _clock: pygame clock
    """
    colors = {
        "white": (255, 255, 255),
        "red": (238,59,59),
        "blue": (0,0,205),
        "gray": (119,136,153),
    }

    def __init__(self, field):
        super().__init__(field)

        # Initialize a pygame window and add it as an attribute
        pygame.init()
        self._fps = 40
        self._window = pygame.display.set_mode((field.window_x, field.window_y))
        pygame.display.set_caption("Game: ")
        self._clock = pygame.time.Clock()
        self._window.fill((255, 255, 255))

    @property
    def fps(self):
        """
        Returns private _fps attribute.
        """
        return self._fps

    def draw_character_as_circle(self, char, color):
        """
        Draws a character as a circle on the pygame screen.

        Args:
            char (Character): Character instance to be drawn on screen
            color (tuple of integers): RGB color tuple
        """
        char_color = hsv2rgb(char.size/10,1.0,0.75)
        pygame.draw.circle(self._window, char_color, char.position, 30)

    def draw(self):
        # VERY IMPORTANT but maybe belongs in the game loop?
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        # draw AI players
        for aip in self._field.ai_players:
            self.draw_character_as_circle(aip, self.colors["red"])

        # draw Player 1
        self.draw_character_as_circle(self._field.player, self.colors["blue"])

        # # draw growth progress bar
        # health_progress = self._field.player.growth_progress
        # pygame.draw.rect(self._window, self.colors["gray"],\
        #     pygame.Rect(0, 0, 20, self.field.window_y * health_progress/100),\
        #     border_top_right_radius=5, border_bottom_right_radius=5)

        # update display
        pygame.display.update()
        self._window.fill(self.colors["white"])

        # timekeeping
        self._clock.tick(self._fps)
