""" Define game sprites for PONG game

"""
import random

import pygame

from arcademl import utils
from arcademl.pong import ml

random.seed()

PLAYER_LEFT = 0
PLAYER_RIGHT = 1
BALL_SPEED = [0.40, 0.30]
PLAYER_SPEED = 0.25
# We collect game information every #COLLECT_PERIOD frames
COLLECT_PERIOD = 5
# Types of players
PLAYER_MANUAL = 0  # Controlled by the user
PLAYER_AUTO = 1  # Controlled by some simple pre-defined heuristics
PLAYER_ML = 2  # Controlled by a ML model
# Types of movement
MOVEMENT_NO = "No Movement"
MOVEMENT_UP = "Move up"
MOVEMENT_DOWN = "Move down"


class PongBall(pygame.sprite.Sprite):
    """Sprite representing Pong ball"""

    def __init__(self):
        super(PongBall, self).__init__()
        self.image = utils.load_image("ball.png", True)
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.speed = [*BALL_SPEED]
        # Draw the ball in the center of te screen
        self.rect.centerx = utils.WINDOW_WIDTH / 2
        self.rect.centery = utils.WINDOW_HEIGHT / 2

    def bounce(self, axis, time):
        self.speed[axis] = -(self.speed[axis] + random.uniform(-0.02, 0.02))
        self.rect.centerx += self.speed[axis] * time

    def update(self, time, lplayer, rplayer):
        """Update ball position, detect collisions and update
        scores from players.

        This function is executed for every frame.

        """
        # Update position of the ball
        self.rect.centerx += self.speed[0] * time
        self.rect.centery += self.speed[1] * time
        # Detect collision with the left wall
        if self.rect.left <= 1:
            rplayer.point()  # Right player scored
            self.bounce(0, time)
        # Detect collision with the right wall
        if self.rect.right >= utils.WINDOW_WIDTH - 1:
            lplayer.point()  # Left player scored
            self.bounce(0, time)

        # Detect collision top or bottom
        if self.rect.top <= 1 or self.rect.bottom >= utils.WINDOW_HEIGHT - 1:
            self.bounce(1, time)
        # Detect collision with a player
        cleft = pygame.sprite.collide_rect(self, lplayer)
        cright = pygame.sprite.collide_rect(self, rplayer)
        if cleft or cright:
            self.bounce(0, time)
        return


class PongPlayer(pygame.sprite.Sprite):
    """Pong Player sprite representing a paddle."""

    def __init__(self, position: int, ptype: int = PLAYER_MANUAL):
        super(PongPlayer, self).__init__()
        self.image = utils.load_image("paddle.png")
        self.rect = self.image.get_rect()  # type: ignore
        self.rect.centerx = 25
        if position == PLAYER_RIGHT:
            self.rect.centerx = utils.WINDOW_WIDTH - 25
        self.position = position
        self.rect.centery = utils.WINDOW_HEIGHT / 2
        self.ptype = ptype
        self.speed = PLAYER_SPEED
        self.collect = False
        self.reset()

    def reset(self):
        self.data = []
        self.score = 0
        self.counter = 0
        self.rect.centery = utils.WINDOW_HEIGHT / 2

    def point(self):
        """Annotate a point for the player"""
        self.score += 1

    def ballApproaching(self, ball):
        """Return whether the ball is approaching the player"""
        left = self.position == PLAYER_LEFT and ball.speed[0] < 0
        right = self.position == PLAYER_RIGHT and ball.speed[0] > 0
        return left or right

    def maybeCollect(self, ball, userAction: str):
        """Collect data from current game state if all the needed
        conditions are  met.
        """
        if self.collect:  # Data Collection is active
            # We collected the last time COLLECT_PEIOD frames ago
            if self.counter > COLLECT_PERIOD:
                # Ball is aprroaching the player
                if self.ballApproaching(ball):
                    self.data.append(ml.get_row(self, ball, userAction))
                    self.counter = 0

    def move_up(self, time):
        """Move the player up"""
        new_top = self.rect.top - self.speed * time
        if new_top > 0:
            self.rect.top = new_top

    def move_down(self, time):
        """Move the player down"""
        new_bottom = self.rect.bottom + self.speed * time
        if new_bottom < utils.WINDOW_HEIGHT:
            self.rect.bottom = new_bottom

    def move_manual(self, time, keys, ball):
        """Move the paddle according to the key pressed by the
        user.

        """
        if keys[pygame.K_UP]:
            self.move_up(time)
            self.maybeCollect(ball, MOVEMENT_UP)
        elif keys[pygame.K_DOWN]:
            self.move_down(time)
            self.maybeCollect(ball, MOVEMENT_DOWN)
        else:  # No movement
            self.maybeCollect(ball, MOVEMENT_NO)

    def move_auto_simple(self, time, ball):
        """Move the paddle according to some simple pre-defined
        heuristics"""
        if self.rect.centery > ball.rect.centery:
            self.move_up(time)
        if self.rect.centery < ball.rect.centery:
            self.move_down(time)

    def move_ml(self, time, ball):
        """Move the paddle according to the prediction from a ML
        model

        """
        if self.ballApproaching(ball):
            pred = ml.predict(self, ball)
            if pred == MOVEMENT_UP:
                self.move_up(time)
            elif pred == MOVEMENT_DOWN:
                self.move_down(time)

    def move(self, time, keys, ball):
        """Move the paddle according to the player type"""
        self.counter += 1
        if self.ptype == PLAYER_MANUAL:
            self.move_manual(time, keys, ball)
        elif self.ptype == PLAYER_AUTO:
            self.move_auto_simple(time, ball)
        elif self.ptype == PLAYER_ML:
            self.move_ml(time, ball)
