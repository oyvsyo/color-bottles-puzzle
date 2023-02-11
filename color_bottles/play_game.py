import logging
from argparse import ArgumentParser
from importlib import import_module, util

from color_bottles.core import WorldConfig

LOG_LEVEL = logging.WARNING

logger = logging.getLogger("color_bottles")
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


EXTRA_FRONTENDS = ["pygame"]

frontend_help = f"""
    Visualization of a game, also defines the controls.
    By default - console, but can be other if extras is installed.
    Existing - {', '.join(EXTRA_FRONTENDS)}
    To install extras run pip:
    $ pip install "colors-bottles-puzzle[{EXTRA_FRONTENDS[0]}]"
"""


def get_available_frontends() -> list[str]:
    frontends = ["console"]

    for front in EXTRA_FRONTENDS:
        if util.find_spec(front):
            logger.debug("%s finded", front)
            frontends.append(front)

    return frontends


def get_frontend() -> str:
    return get_available_frontends()[-1]


def run() -> None:
    parser: ArgumentParser = ArgumentParser(
        prog="Color Bottles Game", description="Sort color water puzzle", add_help=False
    )
    parser.add_argument(
        "-f",
        "--frontend",
        choices=get_available_frontends(),
        default=get_frontend(),
        help=frontend_help,
    )
    parser.add_argument(
        "-l",
        "--log_level",
        choices=["NOTSET", "CRITICAL", "DEBUG", "ERROR", "FATAL", "WARNING", "INFO"],
        default=LOG_LEVEL,
        help="Enable logging with level",
    )

    args, _ = parser.parse_known_args()
    logger.setLevel(args.log_level)
    frontend_module_path: str = f"color_bottles.frontend.{args.frontend}_front"

    config = WorldConfig.from_parser(main_parser=parser)

    logger.debug("loading frontend: %s", frontend_module_path)
    frontend = import_module(frontend_module_path)
    logger.debug("loaded frontend: %s", frontend_module_path)

    f_logger = logging.getLogger(frontend_module_path)
    f_logger.addHandler(consoleHandler)

    logger.setLevel(args.log_level)
    f_logger.setLevel(args.log_level)

    frontend.run_game(config=config)


if __name__ == "__main__":
    run()
