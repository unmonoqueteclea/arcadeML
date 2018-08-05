""" Utilities to handle Machine Learning models

"""
import csv

# Change this if you are using a different kind of BigML model
from bigml.ensemble import Ensemble

from arcademl import REPO_ROOT, utils

# IMPORTANT: This requires that you have your BigML username and API
# key in the environment variables BIGML_USERNAME and BIGML_API_KEY
# respectively.
MODEL = Ensemble("shared/ensemble/7FaNlN7s87Bzp9bji07vsFW9ltx")


def store_rows(rows):
    """Append all the generated rows to the csv file"""
    pong = REPO_ROOT / "data" / "pong_data.csv"
    if len(rows) > 0:
        with pong.open("a") as f:
            writer = csv.writer(f)
            writer.writerows(rows)


def get_row(player, ball, action=None):
    """Create a ML-ready instance from current game state"""
    output = [
        # Relative ball X position
        ball.rect.centerx / utils.WINDOW_WIDTH,
        # Relative ball Y position
        ball.rect.centery / utils.WINDOW_HEIGHT,
        # Relative player Y position
        player.rect.centery / utils.WINDOW_HEIGHT,
        # Distance betweeen player and ball (in Y axis)
        player.rect.centery - ball.rect.centery,
        # Ball speed in X axis
        ball.speed[0],
        # Ball speed in Y axis
        ball.speed[1],
    ]
    if action:
        # Collect the moveent that the user did
        output.append(action)
    return output


def predict(player, ball):
    """Predict which should be the next movement of the player"""
    row = get_row(player, ball)
    row_dict = {f"field{i+1}": v for i, v in enumerate(row)}
    output = MODEL.predict(row_dict)
    return output["prediction"]
