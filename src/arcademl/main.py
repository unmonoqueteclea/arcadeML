""" main module that initializes the game

"""
import os

import pygame

from arcademl import menu, utils
from arcademl.pong import pong

# Center the Game Application
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()
display = pygame.display.set_mode((utils.WINDOW_WIDTH, utils.WINDOW_HEIGHT))
clock = pygame.time.Clock()
appview = utils.AppViews.MENU

while True:
    if appview == utils.AppViews.MENU:
        appview = menu.show(display, clock)
    elif appview == utils.AppViews.PONG:
        pong.start(display, clock)
        appview = utils.AppViews.MENU
    elif appview == utils.AppViews.RACING:
        print("Racing game is not ready yet!")
        appview = utils.AppViews.MENU
        pygame.quit()
