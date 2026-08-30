"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class TitleScreenState.
"""

import pygame

from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.World import World
from src.states.gamemode.GameModeNormal import GameModeNormal
from src.states.gamemode.GameModeHard import GameModeHard

class TitleScreenState(BaseState):
    def enter(self) -> None:
        self.world = World()
        self.selected: GameModeNormal = GameModeNormal()
        self.selected_num = 0

    def update(self, dt: float) -> None:
        self.world.update(dt)

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "up" and input_data.pressed:
            self.selected: GameModeNormal = GameModeNormal()
            self.selected_num = 0
        if input_id == "down" and input_data.pressed:
            self.selected: GameModeHard = GameModeHard()
            self.selected_num = 1
        
        if input_id == "confirm" and input_data.pressed:
            self.state_machine.change("count_down", self.selected)

    def render_text_normal(self, surface: pygame.Surface, color: tuple):
        render_text(
            surface,
            "Normal",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            2 * settings.VIRTUAL_HEIGHT / 3,
            color,
            center=True,
            shadowed=True,
        )
        
    def render_text_hard(self, surface: pygame.Surface, color: tuple):
        render_text(
            surface,
            "Hard",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            2.5 * settings.VIRTUAL_HEIGHT / 3,
            color,
            center=True,
            shadowed=True,
        )

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        render_text(
            surface,
            "Flappy Bird",
            settings.FONTS["flappy"],
            settings.VIRTUAL_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        render_text(
            surface,
            "Press Enter to start",
            settings.FONTS["medium"],
            settings.VIRTUAL_WIDTH / 2,
            1.5 * settings.VIRTUAL_HEIGHT / 3,
            settings.COLOR_WHITE,
            center=True,
            shadowed=True,
        )
        
        for i in range(2):
            color = settings.COLOR_YELLOW if self.selected_num == 1 else settings.COLOR_WHITE
            color2 = settings.COLOR_WHITE if self.selected_num == 1 else settings.COLOR_YELLOW
            self.render_text_normal(surface, color2)
            self.render_text_hard(surface, color)
        


