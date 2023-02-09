import logging
import sys
from typing import List, Optional

from color_bottles.core import StackBottle, World

logger = logging.getLogger(__name__)

OFFSET: str = "  "
color_set: List[str] = ["🟥", "🟧", "🟩", "🟦", "🟪", "🟫", "⬜️", "⬛️"]

HELP: str = """
 🟣 Color bottles puzzle game 🧪:
Your task - sort all colors in bottles 
 🕹️ Controls : to pour from bottle 3 to bottle 5 just type '3 5' and enter
If number of bottles less then 10, you can ommit the space 💥
Also you can pour multiple times by 1 hit 🔥 - just type in a row 
like '5671' or '5 6 7 1' - will pour 5 to 6 and then 7 to 1
 🔴 To exit - type 'q'
 🔮 Good luck !!
"""


class GameStateView:
    def __init__(self, world: World) -> None:
        self.world: World = world

    def draw_world(self) -> None:
        print()
        for line_number in range(1, self.world.config.bottle_size + 1):
            line = OFFSET
            for bottle in self.world.bottles:
                idx = bottle.size - (bottle.level + line_number)
                if idx >= 0:
                    line += OFFSET + "|  |" + OFFSET
                else:
                    line += OFFSET + f"|{bottle.container[idx]}|" + OFFSET

            print(line)

        line_with_bottles_numbers = OFFSET * 3 + f"{OFFSET*3} ".join(
            [str(b.name) for b in self.world.bottles]
        )
        print(line_with_bottles_numbers)
        print()


def create_game() -> GameStateView:
    StackBottle.n_bottles = 0
    return GameStateView(World.simple_world(color_set))


def parse_valid_bottles(user_input: str, n_bottles: int) -> List[int]:
    user_input = user_input.strip()

    if n_bottles <= 10:
        inputs = [s for s in user_input.replace(" ", "")]
    else:
        inputs = user_input.split()

    if len(inputs) % 2 != 0:
        if len(inputs) == 1:
            if inputs[0] == "q":
                sys.exit(0)

            print("len % 2 != 0")
            return []

    try:
        bottles_ids = [int(i) for i in inputs]

    except ValueError:
        print(f" ❤️‍🩹 Cant parse {inputs} into ints")
        return []

    for b1, b2 in zip(bottles_ids[:-1], bottles_ids[1:]):
        if b2 == b1 or b1 < 0 or b2 < 0:
            print(" 💔 We do not allow to pour into self or negative bottles")
            return []
        elif b1 >= n_bottles or b2 >= n_bottles:
            print(
                f" 🚧 Bottles number cant be greater or equal of the number of bottles ({n_bottles})"
            )
            return []

    return bottles_ids


def run_game():

    print(HELP)

    state: GameStateView = create_game()
    state.draw_world()

    running: bool = True
    while running:
        turn: str = input(" 🎮 your turn:  ")

        bottles_ids = parse_valid_bottles(turn, len(state.world.bottles))

        if bottles_ids:

            for b1, b2 in zip(bottles_ids[:-1], bottles_ids[1:]):
                state.world.bottles[b1].pour_to(state.world.bottles[b2])

            state.draw_world()

            if state.world.is_done:
                print(" 🏆 You Win Congrats 🎉 !!!")
                play_new_game = input(" 🎁 For new game - type 'n'").strip()
                if play_new_game == "n":
                    state: GameStateView = create_game()
                    state.draw_world()
                else:
                    running = False
