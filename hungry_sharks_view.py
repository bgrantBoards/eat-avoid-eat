"""
Hungry Sharks game view
"""
from abc import ABC, abstractmethod
import sys
import math
from colorsys import hsv_to_rgb
import pygame
from pygame.locals import QUIT
from euclid3 import Vector2


def angle_from_x_axis(vector):
    """
    Return the angle of the vector with respect to the x axis.

    Args:
        vector (Vector2): the vector
    """
    return -math.degrees(math.atan2(vector.y, vector.x))


def hsv2rgb(hue, saturation, vibrance):
    """
    Converts an HSV color to an RGB color.

    Args:
        hue (float): hue value
        saturation (float): saturation value
        vibrance (float): vibrance value

    Returns:
        3-tuple of integers: RGB color
    """
    return tuple(round(i * 255) for i in hsv_to_rgb(hue,saturation,vibrance))


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
        "black": (0,0,0),
        "gold": (255, 215, 0),
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

        # font stuff for displaying text
        pygame.font.init()
        self._font = pygame.font.SysFont('Georgia', 50)

    scale_fac = 1
    images_from_size = {
        1 : (pygame.image.load("images/minnow.gif"), .75),
        2 : (pygame.image.load("images/gold_fish.png"), scale_fac),
        3 : (pygame.image.load("images/clown_fish.png"), scale_fac),
        4 : (pygame.image.load("images/cod.png"), scale_fac),
        5 : (pygame.image.load("images/small_shark.png"), 2.25),
        6 : (pygame.image.load("images/tuna.png"), 2.25),
        7 : (pygame.image.load("images/swordfish.png"), 3.3),
        8 : (pygame.image.load("images/hammerhead.png"), 2.75),
        9 : (pygame.image.load("images/great_white.png"), 6),
        10 : (pygame.image.load("images/whale_shark.png"), 4),
    }
    game_background_image = pygame.image.load("images/background.png")
    win_background_image = pygame.image.load("images/win_background.png")
    lose_background_image = pygame.image.load("images/lose_background.png")

    @property
    def fps(self):
        """
        Returns private _fps attribute.
        """
        return self._fps

    def draw_character_as_circle(self, char, is_player=False):
        """
        Draws a character as a circle on the pygame screen.

        Args:
            char (Character): Character instance to be drawn on screen
            color (tuple of integers): RGB color tuple
        """
        char_color = hsv2rgb(char.size/10,1.0,0.75)
        pygame.draw.circle(self._window, char_color, char.position, 30)
        if is_player:
            border_thick = 3
        else:
            border_thick = 1
        pygame.draw.circle(self._window, self.colors["black"], char.position,\
            30, width = border_thick)

    def draw_character_as_img(self, char):
        """
        Draws a character with an appropriate image on the pygame screen.

        Args:
            char (Character): Character instance to be drawn on screen
        """
        # pick correct image
        img = self.images_from_size[char.size][0]
        scale_fac = self.images_from_size[char.size][1]
        draw_height = 40 * scale_fac
        draw_width = draw_height * img.get_rect().width / img.get_rect().height
        img = pygame.transform.scale(img, (int(draw_width), int(draw_height)))

        # rotate and scale image
        char_angle = angle_from_x_axis(char.velocity)
        if char_angle < -90 or char_angle > 90:
            img = pygame.transform.flip(img, False, True)
        img = pygame.transform.rotate(img, char_angle)
        rect = img.get_rect()

        # Draw image
        self._window.blit(img, char.position - Vector2(rect.width/2, rect.height/2))

    def draw(self):
        # VERY IMPORTANT but maybe belongs in the game loop?
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


        # draw AI players
        for aip in self._field.characters:
            # self.draw_character_as_circle(aip, self.colors["red"])
            self.draw_character_as_img(aip)

        # draw Player 1
        # self.draw_character_as_circle(self._field.player, self.colors["blue"], is_player=True)
        self.draw_character_as_img(self._field.player)

        # draw growth progress bar
        health_progress = self._field.player.growth_progress
        pygame.draw.rect(self._window, self.colors["gray"],\
            pygame.Rect(0, 0, 20, self.field.window_y * health_progress/100),\
            border_top_right_radius=5, border_bottom_right_radius=5)

        # update display
        pygame.display.update()
        # self._window.fill(self.colors["white"])
        self._window.blit(self.game_background_image, Vector2(0,0))

        # timekeeping
        self._clock.tick(self._fps)

    def display_text_screen(self, text):
        """
        Displays a white screen with text in the center.

        Args:
            text (string): the text
        """
        self._window.fill(self.colors["white"])

        # This creates a new object on which you can call the render method.
        textsurface = self._font.render(text, False, (0, 0, 0))

        # This creates a new surface with text already drawn onto it.
        # At the end you can just blit the text surface onto your main screen.
        self._window.blit(textsurface,(self.field.window_x/2,self.field.window_y/2))

        pygame.display.update()
    
    def display_img_screen(self, img):
        """
        Displays an image filling the whole screen.

        Args:
            img (Pygame Image): the image
        """
        img = pygame.transform.scale(img, (self._field.window_x, self._field.window_y))
        self._window.blit(img, Vector2(0,0))

        pygame.display.update()

    def win_screen(self):
        """
        Display win screen and quit game on user input.
        """
        self.display_img_screen(self.win_background_image)

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            self._clock.tick(self._fps)

    def lose_screen(self):
        """
        Display lose screen and quit game on user input.
        """
        self.display_img_screen(self.lose_background_image)

        done = False
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            self._clock.tick(self._fps)
