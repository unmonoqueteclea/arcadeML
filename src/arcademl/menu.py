""" Game Selection menu """
import pygame

from arcademl import utils

MENU_OPTION_PONG = 0
MENU_OPTION_RACING = 1
MENU_OPTION_QUIT = 2

MENU_OPTIONS: dict[int, dict] = {
    MENU_OPTION_PONG: {"name": "PONG", "view": utils.AppViews.PONG},
    MENU_OPTION_RACING: {"name": "RACING", "view": utils.AppViews.RACING},
    MENU_OPTION_QUIT: {"name": "QUIT", "view": None},
}


def _menu_entry(display, title, posy, selected):
    # Generate a render a menu entry
    color = utils.COLOR_WHITE if selected else utils.COLOR_BLACK
    posx = utils.WINDOW_WIDTH / 2
    text, rect = utils.text_sprite(title, posx, posy, color, 75, "titles")
    display.blit(text, rect)


def _create_title():
    # Generate a render menu ttle
    posx = utils.WINDOW_WIDTH / 2
    posy = 80
    title, title_rect = utils.text_sprite(
        "ArcadeML", posx, posy, utils.COLOR_YELLOW, 80, "titles"
    )
    return title, title_rect


def _handle_event(event, appview, selected: int):
    # Handle user-pressed key
    if event.type == pygame.QUIT:
        pygame.quit()
    elif event.type == pygame.KEYDOWN:
        # Up arrow key
        if event.key == pygame.K_UP:
            selected = max(selected - 1, 0)
        # Down arrow key
        elif event.key == pygame.K_DOWN:
            selected = min(selected + 1, 2)
        # Return key
        if event.key == pygame.K_RETURN:
            if selected == MENU_OPTION_QUIT:
                pygame.quit()
            appview = MENU_OPTIONS[selected]["view"]
    return appview, selected


def _render(display, clock, selected):
    display.fill(utils.COLOR_BLUE)
    display.blit(*_create_title())
    _menu_entry(display, "Pong", 220, selected == MENU_OPTION_PONG)
    _menu_entry(display, "Racing", 290, selected == MENU_OPTION_RACING)
    _menu_entry(display, "Quit", 360, selected == MENU_OPTION_QUIT)
    pygame.display.update()
    clock.tick(utils.FPS)


def show(display, clock):
    """Render game selection menu and handle its associated actions"""
    appview = utils.AppViews.MENU
    # Default option selected is PONG
    selected = MENU_OPTION_PONG
    pygame.display.set_caption("ArcadeML: Games list")
    while appview == utils.AppViews.MENU:
        for event in pygame.event.get():
            appview, selected = _handle_event(event, appview, selected)
        _render(display, clock, selected)
    return appview
