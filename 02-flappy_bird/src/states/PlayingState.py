"""
ISPPV1 2023
Study Case: Flappy Bird

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the definition of the class PlayingState.
"""

from typing import Optional
import pygame


from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text

import settings
from src.Bird import Bird
from src.World import World
from src.PowerUp import PowerUp
from src.states.gamemode.GameMode import GameMode
from src.states.gamemode.GameModeNormal import GameModeNormal
from src.states.gamemode.GameModeHard import GameModeHard

class PlayingState(BaseState):
    def enter(self, gamemode: GameMode,  bird: Bird = None ,world: Optional[World] = None,) -> None:
        self.mode = gamemode  
        self.world = world if world is not None else World(self.mode, True)
        self.world.reset(True)
        self.bird = bird if bird is not None else Bird(
            settings.VIRTUAL_WIDTH / 2 - settings.BIRD_WIDTH / 2,
            settings.VIRTUAL_HEIGHT / 2 - settings.BIRD_HEIGHT / 2,
            settings.BIRD_WIDTH,
            settings.BIRD_HEIGHT,
        )
        self.score = 0
        self.count_mixer_music: float = 6.5
        self.counter = 6
        self.timer = 0.0
        self.collides_powerup: bool = False

    def collides_floor(self):
        if self.bird.get_rect().bottom >= settings.VIRTUAL_HEIGHT:
            if self.world.collides(self.bird.get_rect()):
                settings.SOUNDS["music_powerup"].stop()
                pygame.mixer.music.play(loops=-1)
                settings.SOUNDS["explosion"].play()
                settings.SOUNDS["explosion"].set_volume(0.15)
                settings.SOUNDS["hurt"].play()
                settings.SOUNDS["hurt"].set_volume(0.9)
                self.state_machine.change("count_down", self.mode)
                return
        
    def update(self, dt: float) -> None:
        self.bird.update(dt)
        self.world.update(dt)
        
        if self.world.collides_powerup(self.bird.get_rect()):
            settings.SOUNDS["powerup_take"].play()
            settings.SOUNDS["powerup_take"].set_volume(1.0)
            self.collides_powerup = True
            self.count_mixer_music = 0
            self.counter = 6
            settings.SOUNDS["music_powerup"].play()
            settings.SOUNDS["music_powerup"].set_volume(0.1)
            pygame.mixer.music.stop()
            
        if not self.collides_powerup:
            if self.world.collides(self.bird.get_rect()):
                settings.SOUNDS["explosion"].play()
                settings.SOUNDS["explosion"].set_volume(0.15)
                settings.SOUNDS["hurt"].play()
                settings.SOUNDS["hurt"].set_volume(0.9)
                self.state_machine.change("count_down", self.mode)
                return
        
        if self.count_mixer_music < settings.TIME_POWERUP:
            self.count_mixer_music += dt
            self.timer += dt
            self.bird.powerup = True
            self.collides_floor()
            if self.timer >= 1.0:
                self.timer = 0
                self.counter -= 1
            if self.count_mixer_music >= settings.TIME_POWERUP:
                self.collides_powerup = False
                self.bird.powerup = False
                pygame.mixer.music.play(loops=-1)
        
        
        if self.world.update_scored(self.bird.get_rect()):
            self.score += 1
            settings.SOUNDS["score"].play()

    def render(self, surface: pygame.Surface) -> None:
        self.world.render(surface)
        self.bird.render(surface)

        if self.collides_powerup:
            render_text(
                surface,
                str(self.counter),
                settings.FONTS["flappy"],
                40,
                40,
                settings.COLOR_WHITE,
                shadowed=True
            )
    
        render_text(
            surface,
            f"Score: {self.score}",
            settings.FONTS["flappy"],
            20,
            10,
            settings.COLOR_WHITE,
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        self.mode.move_bird(self.bird, input_id, input_data)
        if input_id == "jump" and input_data.pressed:
            self.bird.jump()
        if input_id == "pause_tab" and input_data.pressed:
            self.state_machine.change(
                "pause",
                self.mode,
                self.bird,                
                self.world,
                score=self.score
            )
