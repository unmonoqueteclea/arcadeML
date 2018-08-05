# -*- coding: utf-8 -*-
"""
title           :main.py
description     :Main module
author          :Pablo Gonzalez Carrizo (unmonoqueteclea)
date            :20180804
notes           :
python_version  :3.6
"""

import os
import random
from threading import Thread

import ML_engines
import models
import numpy as np
import util
from util import pygame

# Checks for previously created models
model_pong = ML_engines.get_model("pong")
model_racing = ML_engines.get_model("racing")
# Set PyGame Initialization


# Set PyGame Resolution

# Game Frame Rate

# Main menu VISIBLE
menu = util.MENU_MAIN


# S
# Shows menu of the game
def game_menu(game):
    global menu
    # Selected menu option
    selected = util.SELECTED_AUTO
    font = util.get_font("titles")
    pygame.display.set_caption("Pygame ML games")
    while menu == util.MENU_PONG or menu == util.MENU_RACING:
        for event in pygame.event.get():
            menu, selected = games_menu_event(event, menu, selected, game)
        # Menu options text
        screen.fill(util.blue)
        title, title_rect = util.text_format(
            util.GAME_NAMES[game], font, 80, util.yellow
        )

        text_auto, auto_rect = util.text_format(
            "Auto Play", font, 75, util.black
        )
        text_train, start_rect = util.text_format(
            "Train again", font, 75, util.black
        )
        text_quit, quit_rect = util.text_format(
            "Back to menu", font, 75, util.black
        )
        # Selected menu option in white
        if selected == util.SELECTED_AUTO:
            text_auto, auto_rect = util.text_format(
                "Auto Play", font, 75, util.white
            )
        if selected == util.SELECTED_TRAIN:
            text_train, start_rect = util.text_format(
                "Train again", font, 75, util.white
            )
        if selected == util.SELECTED_BACK:
            text_quit, quit_rect = util.text_format(
                "Back to menu", font, 75, util.white
            )
        # Draws text
        screen.blit(title, (util.WIDTH / 2 - (title_rect[2] / 2), 80))
        screen.blit(text_auto, (util.WIDTH / 2 - (auto_rect[2] / 2), 230))
        screen.blit(text_train, (util.WIDTH / 2 - (start_rect[2] / 2), 290))
        screen.blit(text_quit, (util.WIDTH / 2 - (quit_rect[2] / 2), 350))
        pygame.display.update()
        clock.tick(util.FPS)


# Process game menu event
def games_menu_event(event, menu, selected, game):
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    # On press key
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            selected = max(selected - 1, util.SELECTED_AUTO)
        elif event.key == pygame.K_DOWN:
            selected = min(selected + 1, util.SELECTED_BACK)
        elif event.key == pygame.K_RETURN:
            menu = util.GAME_MENU_OPTIONS[selected][game]
    return menu, selected


# Racing game
def racing_game(auto):
    """
    Code  from: http://101computing.net/pygame-tutorial-adding-more-sprites/
    with some modifications
    """
    global menu  # Menu option
    data = []
    counter = 0  # Frames counter
    SPEED = 3  # Car speed
    screen = pygame.display.set_mode((util.WIDTH, util.HEIGHT))
    pygame.display.set_caption("Racing game")
    sprite_list = pygame.sprite.Group()
    # Info text
    info_text = "(r) Reset     (q) quit"
    info, info_rect = models.text(
        info_text, 530, 450, color=util.white, size=12
    )
    rows_text = f"{len(data)} rows collected"
    rows, rows_rect = models.text(rows_text, 530, 20, color=util.white, size=12)
    # Player Car
    playerCar = models.Car(util.red, 60, 80, 70)
    playerCar.rect.x = 160
    playerCar.rect.y = util.HEIGHT - 100
    # Othe player cars
    car1 = models.Car(util.green, 60, 80, random.randint(50, 100))
    car1.rect.x = 60
    car1.rect.y = -100
    car2 = models.Car(util.blue, 60, 80, random.randint(50, 100))
    car2.rect.x = 160
    car2.rect.y = -600
    car3 = models.Car(util.yellow, 60, 80, random.randint(50, 100))
    car3.rect.x = 260
    car3.rect.y = -300
    car4 = models.Car(util.green, 60, 80, random.randint(50, 100))
    car4.rect.x = 360
    car4.rect.y = -900
    # Add the cars to the list of objects
    sprite_list.add(playerCar)
    sprite_list.add(car1)
    sprite_list.add(car2)
    sprite_list.add(car3)
    sprite_list.add(car4)
    # Coming cars group
    coming_cars = pygame.sprite.Group()
    coming_cars.add(car1)
    coming_cars.add(car2)
    coming_cars.add(car3)
    coming_cars.add(car4)
    # Allowing the user to close the window...
    running = True
    clock = pygame.time.Clock()
    while running:
        if counter % 10 == 0:
            rows_text = f"{len(data)} rows collected"
            rows, rows_rect = models.text(
                rows_text, 530, 20, color=util.white, size=12
            )
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                running = False
                menu = util.MENU_RACING
        keys = pygame.key.get_pressed()
        # Pressed q KEY
        if keys[pygame.K_q]:
            if auto:
                # Quit
                running = False
                menu = util.MENU_RACING
            else:
                # Save collected data and start training
                running = False
                header = "PlayerPos, Car1, Car2, Car3, Car4, Movement"
                np.savetxt(
                    "train_racing.csv",
                    data,
                    delimiter=",",
                    comments="",
                    header=header,
                )
                thread = Thread(target=racing_train)
                thread.start()
                menu = util.TRAINING_SCREEN
        # Pressed r KEY
        if keys[pygame.K_r]:
            # Reset
            running = False
            data = []
        # Pressed DOWN KEY
        elif keys[pygame.K_DOWN]:
            SPEED -= 0.05
        # Pressed UP KEY
        elif keys[pygame.K_UP]:
            SPEED += 0.05
        # Move player car
        if auto:
            playerCar.autoMove(model_racing, coming_cars)
        else:
            playerCar.move(keys, data, coming_cars)
        # Game Logic
        for car in coming_cars:
            car.moveForward(SPEED)
            if car.rect.y > util.HEIGHT:
                # Regenerates cars
                car.changeSpeed(random.randint(70, 90))
                car.repaint(random.choice(util.CAR_COLORS))
                car.rect.y = random.randint(-700, -100)
        # Detects car collisions
        car_collision_list = pygame.sprite.spritecollide(
            playerCar, coming_cars, False
        )
        if len(car_collision_list) > 0:
            crash_text = "CRASH!!"
        else:
            crash_text = " "
        crash, crash_rect = models.text(
            crash_text, 540, 200, color=util.white, size=30
        )

        sprite_list.update()
        # Drawing on Screen
        screen.fill((0, 100, 0))
        # Draw The Road
        pygame.draw.rect(screen, util.gray, [40, 0, 400, util.HEIGHT])
        # Draw Line painting on the road
        pygame.draw.line(screen, util.white, [140, 0], [140, util.HEIGHT], 5)
        # Draw Line painting on the road
        pygame.draw.line(screen, util.white, [240, 0], [240, util.HEIGHT], 5)
        # Draw Line painting on the road
        pygame.draw.line(screen, util.white, [340, 0], [340, util.HEIGHT], 5)
        # Now let's draw all the sprites in one go
        sprite_list.draw(screen)
        # Draw Text
        screen.blit(info, info_rect)
        screen.blit(rows, rows_rect)
        screen.blit(crash, crash_rect)
        # Refresh Screen
        pygame.display.flip()
        # Number of frames per second
        clock.tick(util.FPS)


# Pong game


# Reset pong game


# Training pong
def pong_train():
    global menu, model_pong
    dataset = ML_engines.createPongDataset(type=util.ML_BIGML)
    # Create and train deep learning model
    model_pong = ML_engines.createPongModel(dataset, type=util.ML_BIGML)
    menu = util.MENU_PONG


# Training racing
def racing_train():
    global menu, model_racing
    dataset = ML_engines.createRacingDataset(type=util.ML_BIGML)
    # Create and train deep learning model
    model_racing = ML_engines.createRacingModel(dataset, type=util.ML_BIGML)
    menu = util.MENU_RACING


def train_screen():
    global menu
    font = util.get_font("titles")
    font2 = util.get_font("normal")
    text_wait, wait_rect = util.text_format("WAIT", font, 75, util.white)
    text_wait2, wait_rect2 = util.text_format(
        "Training model....", font2, 35, util.white
    )
    text_wait3, wait_rect3 = util.text_format(
        "Using backend: BigML", font2, 20, util.white
    )

    while menu == util.TRAINING_SCREEN:
        screen.fill(util.blue)
        screen.blit(text_wait, (util.WIDTH / 2 - (wait_rect[2] / 2), 60))
        screen.blit(text_wait2, (util.WIDTH / 2 - (wait_rect2[2] / 2), 220))
        screen.blit(text_wait3, (util.WIDTH / 2 - (wait_rect3[2] / 2), 270))
        pygame.display.update()
        clock.tick(util.FPS)


# Initialize the Game
while True:
    if menu == util.MENU_MAIN:
        main_menu()
    elif menu == util.MENU_PONG:
        game_menu(util.MENU_PONG)
    elif menu == util.MENU_TRAIN_PONG:
        # Train Pong
        pong_game(auto=False)
    elif menu == util.MENU_PLAY_PONG:
        # Autoplay pong
        if model_pong is not None:
            pong_game(auto=True)
        else:
            util.popupmsg("You should train a model first!")
            menu = util.MENU_PONG
    elif menu == util.TRAINING_SCREEN:
        # Training model waiting screen
        train_screen()
    elif menu == util.MENU_RACING:
        game_menu(util.MENU_RACING)
    elif menu == util.MENU_TRAIN_RACING:
        racing_game(auto=False)
    elif menu == util.MENU_PLAY_RACING:
        if model_racing is not None:
            racing_game(auto=True)
        else:
            util.popupmsg("You should train a model first!")
            menu = util.MENU_RACING
