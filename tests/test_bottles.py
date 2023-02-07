import pytest

from color_bottles.core import StackBottle, BottleException


def test_bottle_init():
    bottle = StackBottle(size=3)


def test_bottle_add_and_level():
    bottle = StackBottle(size=3)
    bottle.add(1)
    bottle.add(1)

    assert bottle.level == 2


def test_bottle_is_fool():
    bottle = StackBottle(size=2)
    bottle.add(2)
    bottle.add(2)
    bottle.add(2)

    assert bottle.is_full
    assert bottle.level == 2


def test_bottle_add_another_kind():
    bottle = StackBottle(size=2)
    bottle.add(1)
    bottle.add(2)

    assert not bottle.is_full
    assert bottle.level == 1
