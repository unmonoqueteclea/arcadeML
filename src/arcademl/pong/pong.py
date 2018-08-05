import pygame

from arcademl import utils
from arcademl.pong import ml, sprites


def _collected_rows_text(rows, screen):
    # Create and render a text with information about the collected rows
    info_text = f"Collected {len(rows)} rows"
    info, info_rect = utils.text_sprite(
        info_text, 90, 420, color=utils.COLOR_WHITE, size=12
    )
    screen.blit(info, info_rect)


def _score_texts(lplayer, rplayer, screen):
    # Create and render the score of the left player
    text = str(lplayer.score)
    posX = utils.WINDOW_WIDTH / 4
    lp, lp_rect = utils.text_sprite(text, posX, 40, utils.COLOR_WHITE, 25)
    # Create and render the score of the right player
    text = str(rplayer.score)
    posX = utils.WINDOW_WIDTH - utils.WINDOW_WIDTH / 4
    rp, rp_rect = utils.text_sprite(text, posX, 40, utils.COLOR_WHITE, 25)
    screen.blit(lp, lp_rect)
    screen.blit(rp, rp_rect)


def _reset(ball, lplayer, rplayer):
    # Reset game information
    lplayer.reset()
    rplayer.reset()
    ball.reset()


def start(screen, clock):
    """Start rendering Pong game"""
    pygame.display.set_caption("ArcadeML: Pong")
    background = utils.load_image("background.png")
    # Create sprite for the ball
    ball = sprites.PongBall()
    # Create sprites for left and right player
    lplayer = sprites.PongPlayer(sprites.PLAYER_LEFT, sprites.PLAYER_ML)  # noqa
    rplayer = sprites.PongPlayer(sprites.PLAYER_RIGHT, sprites.PLAYER_ML)
    # Additional information
    itext = "(c) Toggle data collection    (r) Reset    (q) quit"
    info, info_rect = utils.text_sprite(itext, 140, 450, utils.COLOR_WHITE, 12)
    running = True
    while running:
        time = clock.tick(utils.FPS)
        keys = pygame.key.get_pressed()
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                pygame.quit()
        # Pressed 'r', reset information
        if pygame.key.get_pressed()[pygame.K_r] != 0:
            _reset(ball, lplayer, rplayer)
        # Pressed 'c'. Toggle data collection
        elif pygame.key.get_pressed()[pygame.K_c] != 0:
            lplayer.collect = not lplayer.collect
            rplayer.collect = not lplayer.collect
        # Pressed 'q'. Quit, but store collected data before
        elif pygame.key.get_pressed()[pygame.K_q] != 0:
            running = False
            ml.store_rows(lplayer.data)
            ml.store_rows(rplayer.data)
        # Update position and velocity of ball
        ball.update(time, lplayer, rplayer)
        lplayer.move(time, keys, ball)
        rplayer.move(time, keys, ball)
        # Drawing sprites
        screen.blit(background, (0, 0))
        _score_texts(lplayer, rplayer, screen)
        screen.blit(ball.image, ball.rect)
        screen.blit(lplayer.image, lplayer.rect)
        screen.blit(rplayer.image, rplayer.rect)
        screen.blit(info, info_rect)
        _collected_rows_text(lplayer.data, screen)
        pygame.display.flip()
