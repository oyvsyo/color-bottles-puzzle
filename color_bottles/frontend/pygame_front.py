import logging
from typing import List, Optional, Tuple

import pygame

from color_bottles.core import StackBottle, World, WorldConfig

logger: logging.Logger = logging.getLogger(__name__)


#  --- pygame stuff
pygame.init()
screen: pygame.surface.Surface = pygame.display.set_mode((980, 480))
clock = pygame.time.Clock()
sysfont: pygame.font.Font = pygame.font.SysFont("chalkdusterttf", 24)

#  --- colors ----
BLACK = (0, 0, 0)
GRAY_SELECT = (178, 178, 127)
GRAY = (127, 127, 127)
WHITE = (230, 230, 230)
RED = (200, 0, 0)
GREEN = (0, 200, 0)
BLUE = (0, 0, 200)
YELLOW = (200, 200, 0)
CYAN = (0, 200, 200)
MAGENTA = (200, 0, 200)

color_set = [GRAY, WHITE, RED, GREEN, BLUE, YELLOW, CYAN, MAGENTA]

QUAD: int = 50
SELECTED_BORDER: int = 4


class BottleView:
    def __init__(self, bottle: StackBottle, x: int, y: int) -> None:
        self.bottle = bottle
        self.size: int = bottle.size
        self.xy: tuple[int, int, int, int] = (x, y, QUAD, QUAD * self.size)
        self.selected_border: tuple[int, int, int, int] = (
            x - SELECTED_BORDER,
            y - SELECTED_BORDER,
            QUAD + SELECTED_BORDER * 2,
            QUAD * self.size + SELECTED_BORDER * 2,
        )
        #  draw self.rect
        self.rect: pygame.rect.Rect = pygame.draw.rect(screen, BLACK, self.xy)
        self.draw_self()
        logger.debug("Draw bottle %d, %d, %d, %d", *self.xy)

    def draw_self(self):
        # flush any colors
        pygame.draw.rect(screen, BLACK, self.xy)
        # draw self
        self.rect = pygame.draw.rect(
            screen,
            GRAY,
            self.xy,
            3,
        )
        self.draw_colors()

    def draw_colors(self) -> None:
        x, y, width, height = self.xy
        for i, color in enumerate(self.bottle.container, start=1):
            color_y = y + (self.size - i) * QUAD
            pygame.draw.rect(screen, color, (x, color_y, QUAD, QUAD))

    def draw_selected(self):
        x, y, width, height = self.xy
        pygame.draw.rect(
            screen,
            GRAY_SELECT,
            self.selected_border,
            SELECTED_BORDER,
        )

    def draw_deselected(self) -> None:
        x, y, width, height = self.xy
        pygame.draw.rect(
            screen,
            BLACK,
            self.selected_border,
            SELECTED_BORDER,
        )


class GameStateView:
    def __init__(self, config) -> None:
        self.world: World = World(config, color_set)

        self.selected_bottle: Optional[BottleView] = None
        self.bottles_views: List[BottleView] = []
        self.new_game_rect = self.draw_new_game_text()
        self.draw_bottles()
        pygame.display.update()

    def draw_new_game_text(self, text: str = "Click here to start new game") -> pygame.rect.Rect:
        img = sysfont.render(text, True, BLUE)
        return screen.blit(img, (20, 20))

    def draw_bottles(self) -> None:
        for i, bottle in enumerate(self.world.bottles):
            x, y = 2 * QUAD * (i + 1), QUAD

            logger.debug("x = %d", x)

            b_view: BottleView = BottleView(bottle, x, y)
            self.bottles_views.append(b_view)
            logger.debug("Draw bottle %s, %d, %d, bottle_name %d", bottle, x, y, bottle.name)
        pygame.display.update()

    def deselect(self) -> None:
        if self.selected_bottle:
            self.selected_bottle.draw_deselected()
            self.selected_bottle = None
            logger.debug("Deselected")

    def select(self, b_view: BottleView) -> None:
        logger.debug("Selected bottle: %s", b_view.bottle)
        self.selected_bottle = b_view
        self.selected_bottle.draw_selected()


def run_game(config: WorldConfig) -> None:
    state = GameStateView(config)

    game_ended = False
    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                return
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                logger.info(event)
                pos: Tuple[int, int] = pygame.mouse.get_pos()
                logger.debug(pos)

                collided: bool = False

                for b_view in state.bottles_views:
                    if b_view.rect.collidepoint(pos):
                        collided = True
                        logger.debug("[MAINLOOP] Colide with bottle %s", b_view.bottle)
                        if state.selected_bottle and b_view is not state.selected_bottle:
                            logger.debug(
                                "[MAINLOOP] Pour bottle %s to %s",
                                state.selected_bottle.bottle,
                                b_view.bottle,
                            )
                            state.selected_bottle.bottle.pour_to(b_view.bottle)

                            state.selected_bottle.draw_self()
                            b_view.draw_self()

                            state.deselect()

                            text = ""
                            if state.world.is_solved:
                                game_ended = True
                                text = "You Win, Click here to start new game"
                            elif state.world.is_no_move_left:
                                game_ended = True
                                text = "No move left, Click here to start new game"

                            if game_ended:
                                state.new_game_rect = state.draw_new_game_text(text)
                                pygame.display.update()

                        else:
                            logger.debug("[MAINLOOP] Selected bottle %s", b_view.bottle)
                            state.select(b_view)
                        pygame.display.update()
                # not collided but click
                if not collided:
                    state.deselect()
                    pygame.display.update()

                if state.new_game_rect.collidepoint(pos):
                    state = GameStateView(config)

        clock.tick(60)
