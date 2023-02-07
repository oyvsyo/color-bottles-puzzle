from color_bottles.core import BottleException, StackBottle


def test_bottle_init():
    bottle: StackBottle[int] = StackBottle(size=3)
    assert True


def test_bottle_add_and_level():
    bottle: StackBottle[int] = StackBottle(size=3)
    bottle.add(1)
    bottle.add(1)

    assert bottle.level == 2


def test_bottle_is_fool():
    bottle: StackBottle[int] = StackBottle(size=2)
    bottle.add(2)
    bottle.add(2)
    bottle.add(2)

    assert bottle.is_full
    assert bottle.level == 2


def test_bottle_add_another_kind():
    bottle: StackBottle[int] = StackBottle(size=2)
    bottle.add(1)
    bottle.add(2)

    assert not bottle.is_full
    assert bottle.level == 1


def test_pour_to_empty():
    bottle1: StackBottle[int] = StackBottle(size=2)
    bottle2: StackBottle[int] = StackBottle(size=2)

    bottle1.add(1)
    bottle1.pour_to(bottle2)

    assert bottle1.is_empty
    assert bottle2.level == 1


def test_pour_not_equal():
    bottle1: StackBottle[int] = StackBottle(size=2)
    bottle2: StackBottle[int] = StackBottle(size=2)

    bottle1.add(1)
    bottle2.add(2)
    bottle1.pour_to(bottle2)

    assert bottle1.level == 1
    assert bottle2.level == 1
