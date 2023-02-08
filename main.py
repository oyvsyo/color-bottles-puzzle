import logging
import importlib


LOG_LEVEL = logging.DEBUG

logger = logging.getLogger(__name__)
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
logger.setLevel(LOG_LEVEL)


if __name__ == "__main__":
    frontend_module_path: str = "color_bottles.frontend.pygame"

    logger.debug("loading frontend: %s", frontend_module_path)
    frontend = importlib.import_module(frontend_module_path)
    logger.debug("loaded frontend: %s", frontend_module_path)

    f_logger = logging.getLogger(frontend_module_path)
    f_logger.addHandler(consoleHandler)
    f_logger.setLevel(LOG_LEVEL)

    frontend.main()
