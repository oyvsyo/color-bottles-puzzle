# Frontend agnostic main logic of
import logging
import random
from typing import Generic, List, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

logger = logging.getLogger(__name__)


class BottleException(Exception):
    pass


class StackBottle(Generic[T]):

    n_bottles = 0

    def __init__(self, size: int = 4):
        self._size = size
        self._container: List[T] = []

        self.name = StackBottle.n_bottles
        StackBottle.n_bottles += 1

    @property
    def size(self) -> int:
        return self._size

    @property
    def is_full(self) -> bool:
        return self._size == self.level

    @property
    def is_empty(self) -> bool:
        return self.level == 0

    @property
    def level(self) -> int:
        return len(self._container)

    @property
    def is_full_with_one_color(self) -> bool:
        if not self.is_full or self.is_empty:
            return False
        else:
            return self._container[:-1] == self._container[1:]

    def add(self, element: T):
        if self.is_full:
            logger.debug("Bottle is full %s", self)

        elif self.is_empty:
            logger.debug("Added %s to bottle: %s", element, self)
            self._container.append(element)

        elif self._container[-1] != element:
            logger.debug("Elements are not equal %s != %s", self._container[-1], element)

        elif self._container[-1] == element:
            logger.debug("Added %s to bottle: %s", element, self)
            self._container.append(element)

    def insert(self, element: T):
        if self.is_full:
            logger.debug("Bottle is full %s", self)
        else:
            logger.debug("Added %s to bottle: %s", element, self)
            self._container.append(element)

    def can_pour(self, another_bottle: "StackBottle") -> bool:
        if self.is_empty:
            logger.debug("Source bottle is empty %s", self)
            return False
        elif another_bottle.is_full:
            logger.debug("Destination bottle is  %s", another_bottle)
            return False
        elif another_bottle.is_empty:
            return True
        elif self._container[-1] != another_bottle._container[-1]:
            logger.debug("Destination bottle have different element %s", another_bottle)
            return False
        elif another_bottle is self:
            logger.debug("Cannot pour to itself %s", another_bottle)
            return False
        else:
            return True

    def pour_to(self, another_bottle: "StackBottle"):
        while self.can_pour(another_bottle):
            another_bottle.add(self._container.pop())

    def __repr__(self) -> str:
        return f"StackBottle(name={self.name})<{self.level}/{self._size}>:[{self._container}]"

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:
        return self.level


class WorldConfig(BaseModel):
    n_bottles: int
    n_empty: int
    bottle_size: int
    n_collors: int


class World(Generic[T]):
    def __init__(self, config: WorldConfig, color_set: List[T]) -> None:
        self.config: WorldConfig = config
        self.bottles: List[StackBottle[T]] = [
            StackBottle(config.bottle_size) for i in range(config.n_bottles)
        ]

        colors = random.sample(color_set, k=config.n_collors)

        n_full_bottles = config.n_bottles - config.n_empty
        shuffled = colors * (n_full_bottles - 1)
        random.shuffle(shuffled)

        for i, bottle in enumerate(self.bottles[:n_full_bottles]):
            for j in range(bottle.size):
                bottle.insert(shuffled[i * bottle.size + j])

    @property
    def is_done(self) -> bool:
        for bottle in self.bottles:
            if bottle.is_empty or bottle.is_full_with_one_color:
                pass
            else:
                return False
        return True

    @classmethod
    def random_world(cls, color_set) -> "World":
        n_bottles: int = random.randint(3, 7)
        n_empty: int = n_bottles % 2 + 1
        bottle_size: int = n_bottles - 2

        conf: WorldConfig = WorldConfig(
            n_bottles=n_bottles,
            n_empty=n_empty,
            bottle_size=bottle_size,
            n_collors=n_bottles - n_empty,
        )
        return cls(conf, color_set)

    @classmethod
    def simple_world(cls, color_set):

        conf: WorldConfig = WorldConfig(n_bottles=7, n_empty=2, bottle_size=4, n_collors=5)
        return cls(conf, color_set)
