import logging
from typing import List, Optional
import pygame
from pygame.locals import MOUSEBUTTONDOWN, QUIT

from color_bottles.core import StackBottle, World


logger = logging.getLogger(__name__)
logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)
logger.setLevel(logging.DEBUG)


pygame.init()
screen = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

BLACK = (0, 0, 0)
GRAY_SELECT = (178, 178, 127)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

color_set = [GRAY, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]

QUAD: int = 50
SELECTED_BORDER: int = 4


class BottleView:
    def __init__(self, bottle: StackBottle, x: int, y: int, size: int):
        self.bottle = bottle
        self.size = size
        self.xy: tuple[int, int, int, int] = (x, y, QUAD, y + QUAD * size)
        self.selected_border = (
            x - SELECTED_BORDER,
            y - SELECTED_BORDER,
            QUAD + SELECTED_BORDER * 2,
            y + QUAD * size + SELECTED_BORDER * 2,
        )
        self.rect = self.draw_self()
        logger.debug("Draw bottle %d, %d, %d, %d", *self.xy)

    def draw_self(self):
        pygame.draw.rect(screen, BLACK, self.xy)
        return pygame.draw.rect(
            screen,
            GRAY,
            self.xy,
            3,
        )

    def draw_colors(self):
        height = self.xy[-1]
        x = self.xy[0]
        for color in self.bottle._container:
            pygame.draw.rect(
                screen,
                GRAY,
                self.xy,
                3,
            )

    def draw_selected(self):
        x, y, width, height = self.xy
        pygame.draw.rect(
            screen,
            GRAY_SELECT,
            self.selected_border,
            SELECTED_BORDER,
        )
        pygame.display.update()

    def draw_deselected(self):
        x, y, width, height = self.xy
        pygame.draw.rect(
            screen,
            BLACK,
            self.selected_border,
            SELECTED_BORDER,
        )
        pygame.display.update()


class ColorView:
    pass


class GameStateView:
    def __init__(self, world: World):
        self.world: World = world
        self.selected_bottle: Optional[BottleView] = None
        self.bottles_views: List[BottleView] = []

    def draw_bottles(self):
        for i, bottle in enumerate(self.world.bottles):
            x, y = 2 * QUAD * (i + 1), QUAD

            logger.debug("x = %d", x)

            b_view = BottleView(bottle, x, y, bottle.size)
            self.bottles_views.append(b_view)
            logger.debug("Draw bottle %s, %d, %d, bottle_name %d", bottle, x, y, bottle.name)
        pygame.display.update()

    def deselect(self):
        if self.selected_bottle:
            self.selected_bottle.draw_deselected()
            self.selected_bottle = None
            logger.debug("Deselected")

    def select(self, b_view: BottleView):
        logger.debug("Selected bottle: %s", b_view.bottle)
        self.selected_bottle = b_view
        self.selected_bottle.draw_selected()


# bottle: BottleView = BottleView(100, 100, 4)
# pygame.display.update()


def main():

    world = World.simple_world(color_set)
    state = GameStateView(world=world)

    state.draw_bottles()

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                logger.info(event)
                pos = pygame.mouse.get_pos()
                logger.debug(pos)

                collided: bool = False

                for b_view in state.bottles_views:
                    if b_view.rect.collidepoint(pos):
                        collided = True
                        logger.debug("[MAINLOOP] Colide with bottle %s", b_view.bottle)
                        if state.selected_bottle:

                            logger.debug(
                                "[MAINLOOP] Pour bottle %s to %s",
                                state.selected_bottle.bottle,
                                b_view.bottle,
                            )
                            state.deselect()
                        else:
                            logger.debug("[MAINLOOP] Selected bottle %s", b_view.bottle)
                            state.select(b_view)
                # not collided but click
                if not collided:
                    state.deselect()

        clock.tick(60)


if __name__ == "__main__":
    main()
