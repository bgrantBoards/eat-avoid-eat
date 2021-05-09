"""
Unit testing for the game
"""

import pytest
from character import *
from hungry_sharks_game import *
from hungry_sharks_field import *
from character_controller import *
from euclid3 import Vector2

# CHARACTER TESTING

def test_character_grow():
    """
    Test that growing the player increases their growth progress.
    """
    # create a size 1 player at a position
    test_player = Player(1, Vector2(100, 100))

    for i in range(1, 10):
        test_player.grow(120)
        assert test_player.size == i+1

UPDATE_POS_CASES = [
    # (init_pos, velocity, timestep),
    (Vector2(0,0), Vector2(1,0), 1),
    (Vector2(0,0), Vector2(1,0), .5),
    (Vector2(3,4), Vector2(1,0), 1),
    (Vector2(0,0), Vector2(-1,0), 1),
    (Vector2(0,0), Vector2(0,1), 1),
    (Vector2(0,0), Vector2(0,-1), 1),
    (Vector2(0,0), Vector2(1,1), .25),
    (Vector2(0,0), Vector2(1,-1), 5),
]

@pytest.mark.parametrize("init_pos, velocity, timestep", UPDATE_POS_CASES)
def test_update_position(init_pos, velocity, timestep):
    """
    Test that Character's update_pos method properly moves the character based
    on velocity

    Args:
        init_pos (Vector2): initial position of character
        velocity (Vector2): velocity of character
        timestep (float): amount of time over which the velocity is applied
    """
    # create a character
    test_char = Character(0, init_pos.copy())
    test_char.velocity = velocity

    # update character's position
    test_char.update_pos(timestep)

    # check that the position updated correctly
    assert test_char._position == init_pos + velocity*timestep


MOVE_XX_POINT_CASES = [
    # (init_pos, point_to_move_toward),
    (Vector2(0,0), Vector2(16,23)),
    (Vector2(30,40), Vector2(344,2)),
    (Vector2(20,46), Vector2(1,0)),
    (Vector2(73239,9879), Vector2(-34,0)),
    (Vector2(493,45), Vector2(0,28)),
    (Vector2(0,400), Vector2(45,-1)),
    (Vector2(2323,0), Vector2(939,663)),
    (Vector2(69,86), Vector2(827,932)),
]

@pytest.mark.parametrize("init_pos, point", MOVE_XX_POINT_CASES)
def test_move_toward_point(init_pos, point):
    """
    Test that Character's move toward point method changes a character's
    position correctly

    Args:
        init_pos (Vector2): initial position of character
        point ([type]): target point of movement
    """
    # create a character
    test_char = Character(1, init_pos.copy())
    test_char.move_toward_point(point)

    # update character's position
    test_char.move_toward_point(point)

    # check that the position updated correctly
    planned_displacement = (point - init_pos).normalize()
    actual_displacement = (point - test_char._position).normalize()
    assert abs(planned_displacement - actual_displacement) < 0.01

@pytest.mark.parametrize("init_pos, point", MOVE_XX_POINT_CASES)
def test_move_away_from_point(init_pos, point):
    """
    Test that Character's move away from point method changes a character's
    position correctly

    Args:
        init_pos (Vector2): initial position of character
        point ([type]): target point of movement
    """
    # create a character
    test_char = Character(1, init_pos.copy())
    test_char.move_toward_point(point)

    # update character's position
    test_char.move_toward_point(point)

    # check that the position updated correctly
    planned_displacement = -(point - init_pos).normalize()
    actual_displacement = -(point - test_char._position).normalize()
    assert abs(planned_displacement - actual_displacement) < 0.01


def test_player_boost():
    """
    Test that when the player is boosting, their max_speed method behaves
    appropriately
    """
    # create a size 1 player at a position
    test_player = Player(2, Vector2(100, 100))
    test_player._growth_progress = 50

    for _ in range(1, 10):
        test_player.boost = False
        pre_boost_max_speed = test_player.max_speed()
        test_player.boost = True
        post_boost_max_speed = test_player.max_speed()

        assert post_boost_max_speed > pre_boost_max_speed


AIP_RELOCATE_CASES = [
    # aip_pos,
    Vector2(0,1),
    Vector2(40,27),
    Vector2(59,0),
    Vector2(50,20),
    Vector2(34,36),
    Vector2(2653, 473),
    Vector2(284, -372),
    Vector2(38383,1),
]

@pytest.mark.parametrize("aip_pos", AIP_RELOCATE_CASES)
def test_aip_relocate(aip_pos):
    """
    Test that spawning an AI player and calling its relocate method appropriately
    repositions it with respect to the player.

    Args:
        aip_pos (Vector2): aip spawn location
    """
    # create characters
    player = Player(2, Vector2(0,0))
    aip = AIPlayer(7, aip_pos.copy(), Vector2(0,0), "")

    # check whether the AIP should be relocated
    should_relocate = abs(player._position - aip._position) < aip.fov()

    # relocate
    aip.relocate(player, 400, 400)

    # check valid relocation
    if should_relocate:
        assert abs(player._position - aip._position) > aip.fov()
    else:
        assert aip._position == aip_pos


# FIELD

def test_eat():
    """
    Test that the eating method appropriately grows the player and removes the
    AI player.
    """
    # make field with player at center of window
    field = HungrySharksField(1000, 1000, 0)
    # spawn a smaller aip on top of the player
    aip = AIPlayer(1, Vector2(500,500), Vector2(0,0), "")
    field.spawn_new_ai(aip)
    # call win/lose/eat update method on the field
    field.handle_eating_and_win_lose()

    # check aip disappears
    assert aip not in field.characters
    # check player growth progress increases
    assert field.player._growth_progress > 0
    # check new aip spawns
    assert len(field.characters) > 0


def test_win():
    """
    Test that the field can detect a win under appropriate conditions.
    """
    # make field with player at center of window
    field = HungrySharksField(1000, 1000, 0)

    # set player's size > 10
    field.player._size = 11

    # update the field
    field.handle_eating_and_win_lose()

    # check for the Win
    assert field.game_end == "win"


LOSE_CASES = [i for i in range(1, 11)]

@pytest.mark.parametrize("aip_size", LOSE_CASES)
def test_lose(aip_size):
    """
    Test that the field can detect a loss under appropriate conditions.
    """
    # make field with player at center of window
    field = HungrySharksField(1000, 1000, 0)

    # spawn an aip on top of the player
    aip = AIPlayer(aip_size, Vector2(500,500), Vector2(0,0), "")
    field.spawn_new_ai(aip)

    # update the field
    field.handle_eating_and_win_lose()

    # check for the Win
    if aip_size > field.player._size:
        assert field.game_end == "lose"
    else:
        assert field.game_end == ""


BEHAVIOR_STATE_CASES = [
    # (aip_pos, aip_size, aip_velocity, correct_behavior),
    (Vector2(20,20), 1, Vector2(-10,0), "avoid walls"),
    (Vector2(500, 990), 1, Vector2(0,10), "avoid walls"),
    (Vector2(500,20), 1, Vector2(0,-10), "avoid walls"),
    (Vector2(990, 500), 1, Vector2(10,0), "avoid walls"),
    (Vector2(100,100), 5, Vector2(0,0), "wander"),
    (Vector2(200,200), 5, Vector2(0,0), "wander"),
    (Vector2(500,500), 5, Vector2(0,0), "attack"),
    (Vector2(500,500), 1, Vector2(0,0), "flee"),
    (Vector2(480,500), 5, Vector2(0,0), "attack"),
    (Vector2(480,500), 1, Vector2(0,0), "flee"),
]

@pytest.mark.parametrize("aip_pos, aip_size, aip_velocity, correct_behavior", BEHAVIOR_STATE_CASES)
def test_behavior_state_update(aip_pos, aip_size, aip_velocity, correct_behavior):
    """
    Test that the field can update an AI player's behavior state correctly.

    Args:
        aip_pos (Vector2): aip spawn location
        aip_size (int): aip size
        aip_velocity (Vector2): aip's velocity
        correct_behavior (string): the valid behavior given the other conditions
    """
    # make field with player at center of window
    field = HungrySharksField(1000, 1000, 0)

    # spawn an aip at a position
    aip = AIPlayer(aip_size, aip_pos, aip_velocity, "")
    field.spawn_new_ai(aip)

    # update the field
    field.update_ai_behaviors()

    # check for correct behavior state
    assert aip.behavior_state == correct_behavior


NUM_ENEMIES_CASES = [
    # num_enemies,
    0,
    1,
    2,
    8,
]

@pytest.mark.parametrize("num_enemies", NUM_ENEMIES_CASES)
def test_num_enemies(num_enemies):
    """
    Test that the field can count the number of AI players who are larger than
    the player.

    Args:
        num_enemies (int): number of enemies to spawn
    """
    # make field with player at center of window
    field = HungrySharksField(1000, 1000, 0)

    # spawn a number of larger aip's
    for _ in range(num_enemies):
        field.spawn_new_ai(field.get_new_ai(10))

    # check that the correct number is returned from get_num_enemies
    assert field.get_num_enemies() == num_enemies
