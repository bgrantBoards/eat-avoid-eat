from hungry_sharks_view import PyGameView
from hungry_sharks_field import HungrySharksField

def main():
    """
    Runs the game of Hungry Sharks
    """
    field = HungrySharksField(800, 600, 5)
    view = PyGameView(field)

    while True:
        view.draw()


if __name__ == "__main__":
    main()
