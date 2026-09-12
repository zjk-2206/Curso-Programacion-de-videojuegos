"""
ISPPV1 2023
Study Case: Super Martian (Platformer)

Author: Alejandro Mujica
alejandro.j.mujic4@gmail.com

This file contains the class PlayState.
"""

from typing import Dict, Any

import pygame

from gale.camera import Camera
from gale.input_handler import InputData
from gale.state import BaseState
from gale.text import render_text
from gale.timer import Timer

import settings
from src.Clock import Clock
from src.GameLevel import GameLevel
from src.Player import Player
from src.states.entities import player_states


class PlayState(BaseState):
    def enter(self, **enter_params: Dict[str, Any]) -> None:
        self.level = enter_params.get("level", 1)
        self.game_level = enter_params.get("game_level")
        if self.game_level is None:
            self.game_level = GameLevel(self.level)
            pygame.mixer.music.load(
                settings.BASE_DIR / "assets" / "sounds" / "music_grassland.ogg"
            )
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0.1)

        self.tilemap = self.game_level.tilemap
        self.player = enter_params.get("player")
        self.level_timer =  None
        if self.player is None:
            # Resting exactly on the ground tile's surface (row 9, one tile
            # below the platform's top edge) rather than a few pixels into
            # it, so gale.tilemap's one-way platform collision (which
            # requires the entity to already be at/above the surface) picks
            # it up on the very first frame instead of falling through.
            if self.level == 1:
                spawn_y = 9 * self.tilemap.tile_height - 20
            else:
                spawn_y = 27 * self.tilemap.tile_height - 20
            self.player = Player(0, spawn_y, self.game_level)
            self.player.change_state("idle")
            self.player.has_key = False
            self.player.collide_block = False
            self.player.score = 0

        self.camera = enter_params.get("camera")

        if self.camera is None:
            self.camera = Camera(settings.VIRTUAL_WIDTH, settings.VIRTUAL_HEIGHT)
            self.camera.follow(self.player, rate=settings.CAMERA_FOLLOW_RATE)
            self.camera.bounds = self.game_level.get_rect()
            self.camera.x, self.camera.y = self.player.x, self.player.y
            self.camera.update(0)

        self.clock = enter_params.get("clock") 
        if self.clock is None:
            self.clock = Clock(90)

            def countdown_timer():
                self.clock.count_down()

                if 0 < self.clock.time <= 5:
                    settings.SOUNDS["timer"].play()

                if self.clock.time == 0:
                    self.player.change_state("dead")

            self.level_timer = Timer.every(1, countdown_timer)
        else:
            Timer.resume()
        self.collision_block_special: bool = False

    def update(self, dt: float) -> None:
        if self.player.is_dead:
            pygame.mixer.music.stop()
            pygame.mixer.music.unload()
            Timer.clear()
            self.state_machine.change("game_over", self.player)

        self.player.update(dt)

        if self.player.y >= self.tilemap.pixel_height:
            self.player.change_state("dead")

        self.camera.update(dt)
        self.game_level.update(dt)
        
        if self.player.score >= 25 + self.level * 100:
            if self.level_timer is not None:
                self.level_timer.remove()
                self.level_timer = None  
            
                self.game_level.items = [
                    item for item in self.game_level.items 
                    if not item.frame_index in [62, 61, 55, 54]
                    ]
                
        for creature in self.game_level.creatures:
            if self.player.collides(creature):
                self.player.change_state("dead")

        for item in self.game_level.items:
            if not item.active or not item.collidable:
                continue
             
            if self.player.collides(item):
                if hasattr(item, "frame_index") and item.frame_index == 68 and not self.player.has_key and self.player.score >= 25 + self.level * 100:
                    item.on_collide(self.player)
                    if self.player.collide_block and not self.player.has_key:
                        self.game_level.spawn_key(item.x, item.y)
                        self.player.collide_block = False
                else:
                    item.on_collide(self.player)
                    item.on_consume(self.player)
                    
        if self.player.has_key:
            settings.SOUNDS["complete"].play()
            self.state_machine.change("fade_out", level=self.level + 1, game_level=self.game_level, camera=self.camera, player=self.player)

    def render(self, surface: pygame.Surface) -> None:
        self.game_level.render(surface, self.camera)
        self.player.render(surface, self.camera)

        render_text(
            surface,
            f"Score: {self.player.score}",
            settings.FONTS["small"],
            5,
            5,
            (255, 255, 255),
            shadowed=True,
        )
        
        render_text(
            surface,
            f"Goal coins: {25 + self.level * 100}",
            settings.FONTS["small"],
            5,
            20,
            (255, 255, 255),
            shadowed=True,
        )

        render_text(
            surface,
            f"Time: {self.clock.time}",
            settings.FONTS["small"],
            settings.VIRTUAL_WIDTH - 60,
            5,
            (255, 255, 255),
            shadowed=True,
        )

    def on_input(self, input_id: str, input_data: InputData) -> None:
        if input_id == "pause" and input_data.pressed:
            Timer.pause()
            self.state_machine.change(
                "pause",
                level=self.level,
                camera=self.camera,
                game_level=self.game_level,
                player=self.player,
                clock=self.clock,
            )
            #DEBUG
        elif input_id == "enter" and input_data.pressed:
            settings.SOUNDS["complete"].play()
            self.state_machine.change("fade_out", level=self.level + 1, game_level=self.game_level, camera=self.camera, player=self.player)
        else:
            self.player.on_input(input_id, input_data)
