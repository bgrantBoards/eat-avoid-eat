from hungry_sharks_view import PyGameView
from hungry_sharks_field import HungrySharksField
from character_controller import PlayerVelocityController

# def initialize_pygame():


def main():
    """
    Runs the game of Hungry Sharks
    """
    field = HungrySharksField(800, 600, 10)
    view = PyGameView(field)
    # player_control = PlayerVelocityController(field, view)

    while True:
        view.draw()
        # player_control.move()


if __name__ == "__main__":
    main()
