import pygame
import random

from gale.input_handler import InputData
from .GameMode import GameMode 
from src.LogPair import LogPair
from gale.factory import Factory
from typing import List
import settings 

class GameModeHard(GameMode):
    def __init__(self):
        pass
        
    
    def space_log_H(self, dt: float, world):
        world.logs_spawn_timer += dt
        world.powerup_spawn_timer += dt
        if world.logs_spawn_timer >= random.uniform(settings.TIME_TO_SPAWN_LOGS_HARD_1, settings.TIME_TO_SPAWN_LOGS_HARD_2):
            world.logs_spawn_timer = 0.0
            y = max(
                -settings.LOG_HEIGHT + 10,
                min(
                    world.last_log_y + random.randint(-30, 30),
                    settings.VIRTUAL_HEIGHT + 90 - settings.LOG_HEIGHT,
                ),
            )
            world.last_log_y = y
            world.logs.append(world.log_pair_factory.create(settings.VIRTUAL_WIDTH, y, {"can_move" : bool(random.getrandbits(1))}))
            if world.powerup_spawn_timer >= settings.TIME_POWERUP - 5: 
                world.powerup_spawn_timer = 0
                if random.randint(0, settings.PROBABILITY_TO_SPAWN_POWERUP) == 1:
                    y_power = y + settings.LOG_HEIGHT +  (settings.LOGS_GAP / 2) - 10
                    world.powerups.append(world.powerup_factory.create(settings.VIRTUAL_WIDTH, y_power, {"visible": True}))
            
    
    def move_bird(self, bird , input_id: str, input_data: InputData):
        if input_id in ("right", "left"):
            if input_data.pressed:
                bird.vx = (-settings.BIRD_SPEED if input_id == "left" else settings.BIRD_SPEED) 
            elif input_data.released:
                sign = -1 if input_id == "left" else 1
                if bird.vx == sign * settings.BIRD_SPEED:
                    bird.vx = 0
    