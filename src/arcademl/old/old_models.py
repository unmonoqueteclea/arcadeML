# -*- coding: utf-8 -*-
"""
title           :models.py
description     :Classes that represents the different elements of the game
author          :Pablo Gonzalez Carrizo (unmonoqueteclea)
date            :20180802
notes           :
python_version  :3.6
"""

import random

import ML_engines
import pygame
import util


# Racing game car
class Car(pygame.sprite.Sprite):
    # This class represents a car. It derives from the "Sprite" class in Pygame.
    def __init__(self, color, width, height, speed):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Pass in the color of the car, and its x and y position, width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(util.white)
        self.image.set_colorkey(util.white)
        # Initialise attributes of the car.
        self.width = width
        self.height = height
        self.color = color
        self.speed = speed
        # Draw the car (a rectangle!)
        pygame.draw.rect(
            self.image, self.color, [0, 0, self.width, self.height]
        )
        # Instead we could load a proper picture of a car...
        # self.image = pygame.image.load("car.png").convert_alpha()
        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def moveRight(self, pixels):
        self.rect.x += pixels
        if self.rect.x >= 380:
            self.rect.x = 380

    def moveLeft(self, pixels):
        self.rect.x -= pixels
        if self.rect.x <= 40:
            self.rect.x = 40

    def moveForward(self, speed):
        self.rect.y += self.speed * speed / 20

    def moveBackward(self, speed):
        self.rect.y -= self.speed * speed / 20

    def changeSpeed(self, speed):
        self.speed = speed

    def repaint(self, color):
        self.color = color
        pygame.draw.rect(
            self.image, self.color, [0, 0, self.width, self.height]
        )

    def move(self, keys, data, coming_cars):
        movement = util.MOVEMENT_STOP
        if keys[pygame.K_LEFT]:
            self.moveLeft(10)
            movement = util.MOVEMENT_LEFT
        elif keys[pygame.K_RIGHT]:
            self.moveRight(10)
            movement = util.MOVEMENT_RIGHT
        # Create data row
        cars = [car.rect.y for car in coming_cars]
        row = [self.rect.x]
        row.extend(cars)
        row.extend([movement])
        data.append(row)

    def autoMove(self, model, coming_cars):
        data = {
            "PlayerPos": self.rect.x,
            "Car1": coming_cars.sprites()[0].rect.y,
            "Car2": coming_cars.sprites()[1].rect.y,
            "Car3": coming_cars.sprites()[2].rect.y,
            "Car4": coming_cars.sprites()[3].rect.y,
        }
        # Movement prediction from ML engine
        movement = ML_engines.predict(model, data, util.ML_BIGML)[0:3]
        if float(movement) == util.MOVEMENT_LEFT:
            self.moveLeft(10)
        elif float(movement) == util.MOVEMENT_RIGHT:
            self.moveRight(10)


# Pong game ball
class Ball(pygame.sprite.Sprite):
    """
    Ball Sprite from Pong Game
        Attrs:
            - image (pygame.Image): The image of the ball
            - rect (pygame.Rect): Rect of the ball
            - speed (Tuple): Speed in X and Y axes
    """

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        random.seed()
        self.image = util.load_image("images/ball.png", True)
        self.rect = self.image.get_rect()
        self.rect.centerx = util.WIDTH / 2
        self.rect.centery = util.HEIGHT / 2
        self.speed = [0.5, 0.5]

    def update(self, time, playerCPU, player, score):
        """
        Updates ball position and updates the score
        :param time: Comes from clock.tick()
        :param playerCPU: (PlayerCPU) CPU player sprite
        :param player: (Player) Player sprite
        :param score: (Tuple) Score of both players
        :return: new Score updated
        """
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time

        if self.rect.left <= 1:
            # Collision with the left wall
            score[1] += 1
        if self.rect.right >= util.WIDTH - 1:
            # Collision with the right wall
            score[0] += 1
        if self.rect.left <= 1 or self.rect.right >= util.WIDTH - 1:
            # Colllision with walls
            self.speed[0] = -self.speed[0]
            self.rect.centerx += 3 * self.speed[0] * time

        if self.rect.top <= 1 or self.rect.bottom >= util.HEIGHT - 1:
            # Collision top or bottom
            self.speed[1] = -self.speed[1]
            self.rect.centery += 3 * self.speed[1] * time

        if pygame.sprite.collide_rect(self, player):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += 3 * self.speed[0] * time
        if pygame.sprite.collide_rect(self, playerCPU):
            self.speed[0] = -self.speed[0]
            self.rect.centerx += 3 * self.speed[0] * time
        return score


# Pong game player
class Player(pygame.sprite.Sprite):
    """
    Player from Pong Game
    """

    def __init__(self, posX):
        pygame.sprite.Sprite.__init__(self)
        self.image = util.load_image("images/pala.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = posX
        self.rect.centery = util.HEIGHT / 2
        self.speed = 0.4

    def move(self, time, keys, ball, data):
        movement = False
        if self.rect.top > 0:
            if keys[pygame.K_UP]:
                movement = True
                data.append(
                    [
                        ball.rect.centerx / 640,
                        ball.rect.centery / 480,
                        self.rect.centery / 480,
                        ball.speed[1] + 0.5,
                        util.DIRECTION_UPWARDS,
                    ]
                )
                self.rect.centery -= self.speed * time
        if self.rect.bottom < util.HEIGHT:
            if keys[pygame.K_DOWN]:
                movement = True
                data.append(
                    [
                        ball.rect.centerx / 640,
                        ball.rect.centery / 480,
                        self.rect.centery / 480,
                        ball.speed[1] + 0.5,
                        util.DIRECTION_DOWNWARDS,
                    ]
                )
                self.rect.centery += self.speed * time
        if not movement:
            data.append(
                [
                    ball.rect.centerx / 640,
                    ball.rect.centery / 480,
                    self.rect.centery / 480,
                    ball.speed[1] + 0.5,
                    util.DIRECTION_STILL,
                ]
            )

    def cpu(self, time, ball):
        # Auto algorithmic pong player (without Machine Learning)
        self.speed = [0, 0.5]
        if ball.speed[0] >= 0 and ball.rect.centerx >= util.WIDTH / 2:
            if self.rect.centery > ball.rect.centery:
                self.rect.centery -= self.speed[1] * time
            if self.rect.centery < ball.rect.centery:
                self.rect.centery += self.speed[1] * time

    def autoMove(self, time, model, ball):
        # ML auto move
        data = {
            "BallX": ball.rect.centerx / 640,
            "BallY": ball.rect.centery / 480,
            "PaddlePosition": self.rect.centery / 480,
            "BallSpeed": ball.speed[1] + 0.5,
        }
        # Predict next movement
        movement = ML_engines.predict(model, data, util.ML_BIGML)[0:3]
        # Move Downwards
        if float(movement) == -1 and self.rect.bottom <= util.HEIGHT - 20:
            self.rect.centery += self.speed * time
        # Move Upwards
        elif float(movement) == 1 and self.rect.top >= 20:
            self.rect.centery -= self.speed * time


# Creates text sprite
