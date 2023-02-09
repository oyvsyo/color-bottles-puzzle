from color_bottles.core import StackBottle


def test_bottle_init():
    bottle: StackBottle[int] = StackBottle(size=3)
    assert True


def test_bottle_insert_and_level():
    bottle: StackBottle[int] = StackBottle(size=3)
    bottle.insert(1)
    bottle.insert(1)

    assert bottle.level == 2


def test_pour_to_empty():
    bottle1: StackBottle[int] = StackBottle(size=2)
    bottle2: StackBottle[int] = StackBottle(size=2)

    bottle1.insert(1)
    bottle1.pour_to(bottle2)

    assert bottle1.is_empty
    assert bottle2.level == 1


def test_pour_not_equal():
    bottle1: StackBottle[int] = StackBottle(size=2)
    bottle2: StackBottle[int] = StackBottle(size=2)

    bottle1.insert(1)
    bottle2.insert(2)
    bottle1.pour_to(bottle2)

    assert bottle1.level == 1
    assert bottle2.level == 1
