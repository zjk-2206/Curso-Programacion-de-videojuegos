"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class World: the scrolling
background/ground, and the log pairs the bird must fly through.
"""

import random
from typing import List

import pygame

from gale.factory import Factory

import settings
from src.LogPair import LogPair
from src.states.gamemode.GameMode import GameMode
from src.states.gamemode.GameModeNormal import GameModeNormal
from src.states.gamemode.GameModeHard import GameModeHard
from src.PowerUp import PowerUp 
class World:
    def __init__(self, parameter: GameMode = None, generate_logs: bool = False) -> None:
        self.background_x: float = 0.0
        self.ground_x: float = 0.0
        self.logs: List[LogPair] = []
        self.logs_spawn_timer: float = 0.0
        self.last_log_y: float = -settings.LOG_HEIGHT + random.randint(0, 80) + 20
        self.log_pair_factory: Factory = Factory(LogPair)
        self.generate_logs = generate_logs
        self.mode = parameter
        self.powerup_spawn_timer: float = 0.0
        self.powerup_factory: Factory = Factory(PowerUp)
        self.powerups: List[PowerUp] = []
        

    def reset(self, generate_logs: bool) -> None:
        self.generate_logs = generate_logs

    def update_scored(self, rect: pygame.Rect) -> bool:
        return any(log_pair.update_scored(rect) for log_pair in self.logs)

    def collides(self, rect: pygame.Rect) -> bool:
        if rect.bottom >= settings.VIRTUAL_HEIGHT:
            return True

        return any(log_pair.collides(rect) for log_pair in self.logs)

    def collides_powerup(self, rect: pygame.Rect) -> bool:
        return any(powerup.collides(rect) for powerup in self.powerups)

    def update(self, dt: float) -> None:

        if self.generate_logs:
            self.mode.space_log_H(dt, self)
            
        for log_pair in self.logs:
            log_pair.update(dt)
        
        for powerup in self.powerups:
            powerup.update(dt)
        
        self.background_x += -settings.BACK_SCROLL_SPEED * dt

        if self.background_x <= -settings.BACKGROUND_LOOPING_POINT:
            self.background_x = 0

        self.ground_x += -settings.MAIN_SCROLL_SPEED * dt

        if self.ground_x <= -settings.VIRTUAL_WIDTH:
            self.ground_x = 0

        self.powerups = [powerup for powerup in self.powerups if not powerup.is_out_of_game()]
            
        self.logs = [log_pair for log_pair in self.logs if not log_pair.is_out_of_game()]


    def render(self, surface: pygame.Surface) -> None:
        surface.blit(settings.TEXTURES["background"], (round(self.background_x), 0))

        for powerup in self.powerups:
            powerup.render(surface)        
        
        for log_pair in self.logs:
            log_pair.render(surface)
        
        surface.blit(
            settings.TEXTURES["ground"],
            (round(self.ground_x), settings.VIRTUAL_HEIGHT - settings.GROUND_HEIGHT),
        )
