"""
Hungry Sharks game view
"""
from character import AIPlayer, Player
from hungry_sharks_field import HungrySharksField
from abc import ABC, abstractmethod
import pygame, sys
from pygame.locals import *
from euclid3 import Vector2


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
        _color1: player's color
        _color2: AI Players' color
        _clock: pygame clock
    """
    colors = {
        "white": (255, 255, 255),
        "red": (238,59,59),
        "blue": (0,0,205),
        "gray": (119,136,153),
    }

    def __init__(self, field):
        self._field = field

        # pygame.display.set_mode((width_of_window,height_of_window))
        self._color1 = (140, 255, 255)
        self._color2 = (0, 0, 0)

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

    def draw_character(self, char, color):
        pygame.draw.circle(self._window, color, char.position, char.size)

    def draw(self):
        # VERY IMPORTANT but maybe belongs in the game loop?
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        # draw Player 1
        self.draw_character(self._field.player, self.colors["blue"])

        # draw AI players
        for aip in self._field.ai_players:
            pygame.draw.circle(self._window, self._color2, aip.position, aip.size)
        

        # growth progress bar
        # pygame.draw.rect(self._window, self.colors["gray"], pygame.Rect(0, 0, 20, self.field.window_y), border_top_right_radius=5, border_bottom_right_radius=5)
        health_progress = self._field.player._growth_progress
        pygame.draw.rect(self._window, self.colors["gray"], pygame.Rect(0, 0, 20, self.field.window_y * health_progress/100), border_top_right_radius=5, border_bottom_right_radius=5)

        # update display
        pygame.display.update()
        self._window.fill(self.colors["white"])

        # timekeeping
        self._clock.tick(self._fps)

