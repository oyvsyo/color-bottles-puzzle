# Frontend agnostic main logic of game
import logging
import random
import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from inspect import signature
from typing import Generic, List, TypeVar

T = TypeVar("T")

logger = logging.getLogger(__name__)


class StackBottle(Generic[T]):
    n_bottles: int = 0

    def __init__(self, size: int = 4) -> None:
        self._size: int = size
        self.container: List[T] = []

        self.name: int = StackBottle.n_bottles
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
        return len(self.container)

    @property
    def is_full_with_one_color(self) -> bool:
        if not self.is_full or self.is_empty:
            return False
        else:
            return self.container[:-1] == self.container[1:]

    def insert(self, element: T) -> None:
        if self.is_full:
            logger.debug("Bottle is full %s", self)
        else:
            logger.debug("Added %s to bottle: %s", element, self)
            self.container.append(element)

    def can_pour(self, another_bottle: "StackBottle") -> bool:
        if self.is_empty:
            logger.debug("Source bottle is empty %s", self)
            return False
        elif another_bottle.is_full:
            logger.debug("Destination bottle is  %s", another_bottle)
            return False
        elif another_bottle.is_empty:
            return True
        elif self.container[-1] != another_bottle.container[-1]:
            logger.debug(
                "Destination bottle %s have different element than source %s", another_bottle, self
            )
            return False
        elif another_bottle is self:
            logger.debug("Cannot pour to itself %s", another_bottle)
            return False
        else:
            return True

    def pour_to(self, another_bottle: "StackBottle") -> None:
        while self.can_pour(another_bottle):
            another_bottle.container.append(self.container.pop())

    def __repr__(self) -> str:
        return f"StackBottle(name={self.name})<{self.level}/{self._size}>:{self.container}"

    def __str__(self) -> str:
        return self.__repr__()

    def __len__(self) -> int:
        return self.level


@dataclass(repr=True, init=True)
class WorldConfig:
    n_bottles: int
    n_empty: int
    bottle_size: int
    n_colors: int

    @classmethod
    def from_parser(cls, main_parser: ArgumentParser) -> "WorldConfig":
        parser = ArgumentParser(parents=[main_parser])

        parser.add_argument("-nb", "--n_bottles", type=int, default=9, help="number of bottles")
        parser.add_argument("-nc", "--n_colors", type=int, default=None, help="number of colors")
        parser.add_argument("-ne", "--n_empty", type=int, default=2, help="number of empty bottles")
        parser.add_argument(
            "-bs",
            "--bottle_size",
            type=int,
            default=4,
            help="size of the bootle, ie how many colors the bottle contain",
        )

        args, _ = parser.parse_known_args()
        args.n_colors = args.n_colors or args.n_bottles - args.n_empty
        kwargs = {
            param: value
            for param, value in vars(args).items()
            if param in signature(cls).parameters.keys()
        }
        logger.debug("World config:")
        logger.debug(kwargs)
        return cls(**kwargs)


class World(Generic[T]):
    def __init__(self, config: WorldConfig, color_set: List[T]) -> None:
        self.config: WorldConfig = config
        self.bottles: List[StackBottle[T]] = [
            StackBottle(config.bottle_size) for i in range(config.n_bottles)
        ]

        if len(color_set) < config.n_colors:
            logger.error(
                "We do not have %d colors, please select n_colors <= %d",
                config.n_colors,
                len(color_set),
            )
            sys.exit(1)
        colors: list[T] = color_set[: config.n_colors]

        n_full_bottles: int = config.n_bottles - config.n_empty
        shuffled: list[T] = colors * config.bottle_size

        random.shuffle(shuffled)

        for i, bottle in enumerate(self.bottles[:n_full_bottles]):
            for j in range(bottle.size):
                bottle.insert(shuffled[i * bottle.size + j])

    @property
    def is_solved(self) -> bool:
        for bottle in self.bottles:
            if bottle.is_empty or bottle.is_full_with_one_color:
                pass
            else:
                return False
        return True

    @property
    def is_no_move_left(self) -> bool:
        for bottle1 in self.bottles:
            for bottle2 in self.bottles:
                if bottle1 is not bottle2:
                    if bottle1.can_pour(bottle2) or bottle2.can_pour(bottle1):
                        return False
        return True

    @classmethod
    def random_world(cls, color_set) -> "World[T]":
        n_bottles: int = random.randint(3, 7)
        n_empty: int = n_bottles % 2 + 1
        bottle_size: int = n_bottles - 2

        conf: WorldConfig = WorldConfig(
            n_bottles=n_bottles,
            n_empty=n_empty,
            bottle_size=bottle_size,
            n_colors=n_bottles - n_empty,
        )
        return cls(conf, color_set)

    @classmethod
    def simple_world(cls, color_set) -> "World[T]":
        conf: WorldConfig = WorldConfig(n_bottles=9, n_empty=2, bottle_size=4, n_colors=7)
        return cls(conf, color_set)
