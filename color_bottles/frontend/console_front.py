import logging
import sys
from typing import List

from color_bottles.core import World, WorldConfig

logger: logging.Logger = logging.getLogger(__name__)

OFFSET: str = "  "
color_set_emoji: List[str] = [
    "๐ฅ",
    "๐ง",
    "๐ฉ",
    "๐ฆ",
    "๐ช",
    "๐ซ",
    "โฌ๏ธ",
    "โฌ๏ธ",
    "๐ธ",
    "๐น",
    "๐ด",
    "๐ ",
    "๐ก",
    "๐ข",
    "๐ต",
    "๐ฃ",
    "โซ๏ธ",
    "โช๏ธ",
    "๐ค",
]

color_set = color_set_emoji

if sys.platform == "win32" or sys.platform == "cygwin":
    from colorama import Back, Style, just_fix_windows_console

    just_fix_windows_console()
    color_set_colorama = [
        c + "  " + Style.RESET_ALL
        for c in [
            Back.GREEN,
            Back.BLUE,
            Back.CYAN,
            Back.RED,
            Back.MAGENTA,
            Back.YELLOW,
            Back.LIGHTBLUE_EX,
            Back.LIGHTWHITE_EX,
            Back.LIGHTGREEN_EX,
            Back.LIGHTYELLOW_EX,
        ]
    ]
    color_set = color_set_colorama


HELP: str = """
 ๐ก๏ธ  Watter color sort puzzle game ๐งช:
Your task - sort all colors in bottles 
 ๐น๏ธ Controls : to pour from bottle `3` to bottle `7` just type `3 7` and enter.  
If number of bottles less then 10, you can ommit the space ๐ฅ   
Also you can pour multiple times by 1 hit ๐ฅ - just type in a row 
like `5718` or `5 7 1 8` - will pour `5` to `7` and then `1` to `8`   
๐ด To exit - type `q`   
๐ฎ Good luck !!  
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
        print(f" โค๏ธโ๐ฉน Cant parse {inputs} into ints")
        return []

    for b1, b2 in zip(bottles_ids[:-1], bottles_ids[1:]):
        if b2 == b1 or b1 < 0 or b2 < 0:
            print(" ๐ We do not allow to pour into self or negative bottles")
            return []
        elif b1 >= n_bottles or b2 >= n_bottles:
            print(
                f" ๐ง Bottles number cant be greater or equal of the number of bottles ({n_bottles})"
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
        turn: str = input(" ๐ฎ your turn:  ")

        bottles_ids: List[int] = parse_valid_bottles(turn, len(state.world.bottles))

        if bottles_ids:
            state_changed = False
            for b1, b2 in zip(bottles_ids[::2], bottles_ids[1::2]):
                cant_pour = state.world.bottles[b1].pour_to(state.world.bottles[b2])
                if cant_pour:
                    print(cant_pour)
                    break
                else:
                    state_changed = True

            if state_changed:
                state.draw_world()

            if state.world.is_solved:
                game_ended = True
                print(" ๐ You Win Congrats ๐ !!!")
            elif state.world.is_no_move_left:
                game_ended = True
                print(" ๐ฃ There is no move left โ๏ธ !!!")

            if game_ended:
                play_new_game: str = input(" ๐ For new game - type 'n'").strip()
                if play_new_game == "n":
                    state: GameStateView = GameStateView(config)  # type: ignore[no-redef]
                    state.draw_world()
                    game_ended = False
                else:
                    running = False
