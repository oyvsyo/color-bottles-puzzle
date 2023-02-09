import logging
import importlib
from argparse import ArgumentParser


LOG_LEVEL = logging.WARNING

logger = logging.getLogger(__name__)
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


def get_installed_frontend() -> str:
    try:
        importlib.import_module("pygame")
        return "pygame"
    except:
        return "console"


def run():

    parser = ArgumentParser(prog="Color Bottles Game", description="Sort colors", epilog="_" * 40)

    parser.add_argument("-f", "--frontend", default=get_installed_frontend())
    parser.add_argument(
        "-l",
        "--log_level",
        choices=["NOTSET", "CRITICAL", "DEBUG", "ERROR", "FATAL", "WARNING", "INFO"],
        default=LOG_LEVEL,
    )

    args = parser.parse_args()

    frontend_module_path: str = f"color_bottles.frontend.{args.frontend}_front"

    logger.debug("loading frontend: %s", frontend_module_path)
    frontend = importlib.import_module(frontend_module_path)
    logger.debug("loaded frontend: %s", frontend_module_path)

    f_logger = logging.getLogger(frontend_module_path)
    f_logger.addHandler(consoleHandler)

    logger.setLevel(args.log_level)
    f_logger.setLevel(args.log_level)

    frontend.run_game()


if __name__ == "__main__":
    run()
