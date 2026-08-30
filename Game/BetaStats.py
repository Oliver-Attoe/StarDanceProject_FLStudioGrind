import pygame
from sys import exit
import math
import Settings
from UI import *
from SOUNDS import *
import Timer
import Tiles
import random
import Waiver
import Dialogue
import webbrowser
import json
import os


timer = Timer.Stopwatch()

level_difficulty = [0 for _ in range(Settings.levels)]
level_time = [0 for _ in range(Settings.levels)]
level_restarts = [-1 for _ in range(Settings.levels)]
level_bullet_count =  [[0, 0] for _ in range(Settings.levels)]


def set_difficulty(key):

    if key == pygame.K_1:
        level_difficulty[Settings.player_level - 1] = 1

    elif key == pygame.K_2:
        level_difficulty[Settings.player_level - 1] = 2

    elif key == pygame.K_3:
        level_difficulty[Settings.player_level - 1] = 3

    elif key == pygame.K_4:
        level_difficulty[Settings.player_level - 1] = 4

    elif key == pygame.K_5:
        level_difficulty[Settings.player_level - 1] = 5

    elif key == pygame.K_6:
        level_difficulty[Settings.player_level - 1] = 6

    elif key == pygame.K_7:
        level_difficulty[Settings.player_level - 1] = 7

    elif key == pygame.K_8:
        level_difficulty[Settings.player_level - 1] = 8

    elif key == pygame.K_9:
        level_difficulty[Settings.player_level - 1] = 9
        



def save_stats():
    data = {
        "levels": []
    }

    for level in range(Settings.levels):
        data["levels"].append({
            "Level": level + 1,
            "difficulty_score": level_difficulty[level],
            "time_beaten": level_time[level],
            "deaths_per_level": level_restarts[level],
            "level_bullet_count": level_bullet_count[level]
        })

    save_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "stats.json"
    )

    with open(save_path, "w") as f:
        json.dump(data, f, indent=4)