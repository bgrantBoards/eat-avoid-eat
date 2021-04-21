"""
Hungry Sharks game view
"""
from character import AIPlayer, Player
from hungry_sharks_field import HungrySharksField
from abc import ABC, abstractmethod
import pygame, sys
from pygame.locals import *


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
    def __init__(self, field):
        self._field = field
        # pygame.display.set_mode((width_of_window,height_of_window))
        self._color1 = (255, 140, 255)
        self._color2 = (0, 0, 0)

        # Initialize a pygame window and add it as an attribute
        pygame.init()
        self._fps = 60
        self._window = pygame.display.set_mode((field.window_x, field.window_y))
        pygame.display.set_caption("Game: ")
        self._clock = pygame.time.Clock()
        self._window.fill((255, 255, 255))

    def draw(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.display.update()

        # draw player 1
        pygame.draw.circle(self._window, self._color1, self.field.player.position, self.field.player.size)
        pygame.display.update()
        self._clock.tick(self._fps)

