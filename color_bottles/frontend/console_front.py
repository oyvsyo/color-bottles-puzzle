import logging
import sys
from typing import List, Optional

from color_bottles.core import StackBottle, World

logger = logging.getLogger(__name__)

OFFSET: str = "  "
color_set: List[str] = ["🟥", "🟧", "🟩", "🟦", "🟪", "🟫", "⬜️", "⬛️"]


class GameStateView:
    def __init__(self, world):
        self.world: World = world

    def draw_world(self):
        print()
        for line_number in range(1, self.world.config.bottle_size + 1):
            line = OFFSET
            for bottle in self.world.bottles:
                idx = bottle.size - (bottle.level + line_number)
                if idx >= 0:
                    line += OFFSET + "|  |" + OFFSET
                else:
                    line += OFFSET + f"|{bottle._container[idx]}|" + OFFSET

            print(line)

        line_with_bottles_numbers = OFFSET * 3 + f"{OFFSET*3} ".join(
            [str(b.name) for b in self.world.bottles]
        )
        print(line_with_bottles_numbers)
        print()


def create_game() -> GameStateView:

    return GameStateView(World.simple_world(color_set))


def main():

    state: GameStateView = create_game()
    state.draw_world()

    running: bool = True
    while running:
        turn: list[str] = input("your turn:  ").strip().split()

        is_invalid_input: bool = False

        b_from, b_to = 0, 0

        if len(turn) != 2:
            if len(turn) == 1:
                if turn[0] == "q":
                    sys.exit(0)
            is_invalid_input = True
            print("len != 2")
        else:
            try:
                b_from, b_to = int(turn[0]), int(turn[1])

                if b_from == b_to or b_from < 0 or b_to < 0:
                    is_invalid_input = True
                    print("We do not allow to pour into self or negative bottles")
                elif b_to >= len(state.world.bottles) or b_from >= len(state.world.bottles):
                    print(
                        f"Bottles number cant be greater or equal of the number of bottles ({len(state.world.bottles)})"
                    )
                    is_invalid_input = True

            except ValueError:
                print(f"Cant parse {turn} into 2 ints")
                is_invalid_input = True

        if is_invalid_input:
            print(
                "Invalit move, enter 2 numbers separated by space,"
                " like '3 1' to pour from 3-rd bottle to 1-st "
            )
        else:
            state.world.bottles[b_from].pour_to(state.world.bottles[b_to])

            state.draw_world()

            if state.world.is_done:
                print("You Win Congrats !!!")
                play_new_game = input("For new game - type 'n'").strip()
                if play_new_game == "n":
                    state: GameStateView = create_game()
                    state.draw_world()
                else:
                    running = False
