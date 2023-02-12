import logging
import sys
from typing import List

from color_bottles.core import World, WorldConfig

logger: logging.Logger = logging.getLogger(__name__)

OFFSET: str = "  "
color_set: List[str] = [
    "🟥",
    "🟧",
    "🟩",
    "🟦",
    "🟪",
    "🟫",
    "⬜️",
    "⬛️",
    "🔸",
    "🔹",
    "🔴",
    "🟠",
    "🟡",
    "🟢",
    "🔵",
    "🟣",
    "⚫️",
    "⚪️",
    "🟤",
]

HELP: str = """
 🌡️  Watter color sort puzzle game 🧪:
Your task - sort all colors in bottles 
 🕹️ Controls : to pour from bottle 3 to bottle 5 just type '3 5' and enter
If number of bottles less then 10, you can ommit the space 💥
Also you can pour multiple times by 1 hit 🔥 - just type in a row 
like '5671' or '5 6 7 1' - will pour 5 to 6 and then 7 to 1
 🔴 To exit - type 'q'
 🔮 Good luck !!
"""


class GameStateView:
    def __init__(self, config) -> None:
        self.world: World = World(config, color_set)

    def draw_world(self) -> None:
        print()
        for line_number in range(1, self.world.config.bottle_size + 1):
            line: str = OFFSET
            for bottle in self.world.bottles:
                idx: int = bottle.size - (bottle.level + line_number)
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


def parse_valid_bottles(user_input: str, n_bottles: int) -> List[int]:
    user_inputs: str = user_input.strip()

    if n_bottles <= 10:
        inputs: list[str] = [s for s in user_inputs.replace(" ", "")]
    else:
        inputs = user_inputs.split()

    if len(inputs) % 2 != 0:
        if len(inputs) == 1:
            if inputs[0] == "q":
                sys.exit(0)

            print("len % 2 != 0")
            return []

    try:
        bottles_ids: list[int] = [int(i) for i in inputs]

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


def run_game(config: WorldConfig) -> None:
    state: GameStateView = GameStateView(config)
    print(HELP)
    state.draw_world()

    game_ended = False
    running: bool = True
    while running:
        turn: str = input(" 🎮 your turn:  ")

        bottles_ids: List[int] = parse_valid_bottles(turn, len(state.world.bottles))

        if bottles_ids:
            for b1, b2 in zip(bottles_ids[:-1], bottles_ids[1:]):
                state.world.bottles[b1].pour_to(state.world.bottles[b2])

            state.draw_world()

            if state.world.is_solved:
                game_ended = True
                print(" 🏆 You Win Congrats 🎉 !!!")
            elif state.world.is_no_move_left:
                game_ended = True
                print(" 📣 There is no move left ⛔️ !!!")

            if game_ended:
                play_new_game: str = input(" 🎁 For new game - type 'n'").strip()
                if play_new_game == "n":
                    state: GameStateView = GameStateView(config)  # type: ignore[no-redef]
                    state.draw_world()
                    game_ended = False
                else:
                    running = False
