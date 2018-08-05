"""Utilties and configuration parameters for building the games

"""
import pathlib
from enum import Enum

import pygame

from arcademl import REPO_ROOT

WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FPS = 30

# List of available colors
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (50, 50, 50)
COLOR_RED = (255, 0, 0)
COLOR_GREEN = (0, 255, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)


class AppViews(Enum):
    """Enumeration with all the available app views"""

    MENU = 0  # Main menu view
    PONG = 1  # Pong game view
    RACING = 2  # Racing game view


FONTS: dict[str, pathlib.Path] = {
    "normal": REPO_ROOT / "assets" / "DroidSans.ttf",
    "titles": REPO_ROOT / "assets" / "EffectsEighty.ttf",
}


def text_sprite(
    text: str,
    posx: int,
    posy: int,
    color: tuple[int, int, int],
    size: int,
    font_name: str = "normal",
) -> tuple[pygame.surface.Surface, pygame.rect.Rect]:
    """Create a text sprite centered in a given position and return
    its surface and its rect
    """
    font = pygame.font.Font(FONTS[font_name], size)
    output = pygame.font.Font.render(font, text, True, color)
    output_rect = output.get_rect()
    output_rect.centerx = posx
    output_rect.centery = posy
    return output, output_rect


def load_image(filename: str, transparent=False):
    """Load an image as a pygame sprite from a filename"""
    filepath = REPO_ROOT / "assets" / filename
    try:
        image = pygame.image.load(str(filepath))
    except pygame.error as message:
        raise SystemExit(message)
    image = image.convert()
    if transparent:
        # We suppose the top left corner is transparent
        color = image.get_at((0, 0))
        image.set_colorkey(color, pygame.RLEACCEL)
    return image
