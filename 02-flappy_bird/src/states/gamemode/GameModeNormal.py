import pygame
import random

from gale.input_handler import InputData
from .GameMode import GameMode 
from src.LogPair import LogPair
from gale.factory import Factory
from typing import List
import settings 

class GameModeNormal(GameMode):
    def __init__(self):
        pass

    def space_log_H(self, dt: float, world):
        world.logs_spawn_timer += dt
        if world.logs_spawn_timer >= settings.TIME_TO_SPAWN_LOGS:
            
            world.logs_spawn_timer = 0.0
            y = max(
                -settings.LOG_HEIGHT + 10,
                min(
                    world.last_log_y + random.randint(-20, 20),
                    settings.VIRTUAL_HEIGHT + 90 - settings.LOG_HEIGHT,
                ),
            )
            world.last_log_y = y
            world.logs.append(world.log_pair_factory.create(settings.VIRTUAL_WIDTH, y, {"can_move": False}))