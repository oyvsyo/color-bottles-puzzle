# Frontend agnostic main logic of
from typing import List, TypeVar, Generic
import logging

T = TypeVar("T")

logger = logging.getLogger(__name__)


class BottleException(Exception):
    pass


class StackBottle:
    def __init__(self, size: int = 4):
        self._size = size
        self._container: List[T] = []

    def __len__(self) -> int:
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

    def __repr__(self) -> str:
        return f"StackBottle<{self.level}/{self._size}>:[{self._container}]"

    def __str__(self) -> str:
        return self.__repr__


# class Element:
#     def __init__(self, kind: int):
#         self._kind = kind

#     def __eq__(self, __o: object) -> bool:
#         return self._kind == __o._kind
