import random
from typing import Any, Callable, List, Optional, TypeVar

import pygame
import random

import settings
from src.definitions.entity import ENTITY_DEFS
from src.world.Room import Room
from src.states.entity.Boss.Boss import Boss
from gale.tilemap import TileMap
from src.world.Doorway import Doorway


class BossRoom(Room):
    def __init__(self, player: TypeVar("Player"), on_game_over: Callable[[], None], name_entitie: str):
        self.entitie_type = name_entitie
        self.player = player
        self.width = settings.MAP_WIDTH
        self.height = settings.MAP_HEIGHT
        self.objects = []
        self.doorways = [] 
        self.tilemap = TileMap(settings.TILE_SIZE, settings.TILE_SIZE, self.width, self.height)
        self.tilemap.add_tileset(settings.TILESET)
        self._generate_walls_and_floors()
        self.render_offset_x = settings.MAP_RENDER_OFFSET_X
        self.render_offset_y = settings.MAP_RENDER_OFFSET_Y
        self.adjacent_offset_x = 0
        self.adjacent_offset_y = 0
        self.entities = []
        self.doorways = [
            Doorway("top", False, self),
            Doorway("bottom", False, self),
            Doorway("left", False, self),
            Doorway("right", False, self),
        ]
        self._doorways_by_direction = {
            doorway.direction: doorway for doorway in self.doorways
        }
        self.chess_generate = False
        self.chess = any
        
        
        self.projectiles = []

    def _generate_entities(self):
        self.entities = []
        definition = ENTITY_DEFS[self.entitie_type]
        
        self.boss = Boss(
            x=settings.VIRTUAL_WIDTH // 2 - 8,
            y=settings.VIRTUAL_HEIGHT // 2 - 8,
            width=16,
            height=16,
            walk_speed=definition.get("walk_speed", 40),
            health=5,
            animation_defs=definition["animations"],
            states={}
        )
        
        self.boss.room = self 

        from src.states.entity.Boss.BossStrongState import BossStrongState
        from src.states.entity.Boss.BossWakeState import BossWakeState
        from src.states.entity.Boss.BossWalkState import BossWalkState
        
        self.boss.state_machine.states = {
            "strong": lambda sm, e=self.boss: BossStrongState(e, sm),
            "wake": lambda sm, e=self.boss: BossWakeState(e, sm),
            "walk": lambda sm, e=self.boss: BossWalkState(e, sm),
        }
        
        self.boss.change_state("strong")
        self.entities.append(self.boss)

    def update(self, dt: float) -> None:
        super().update(dt) 
        
        for fireball in list(self.projectiles):
            fireball.update(dt)
            
            if not fireball.dead and fireball.collides(self.player) and not self.player.invulnerable:
                settings.SOUNDS["hit-player"].play()
                self.player.damage(1)
                self.player.go_invulnerable(1.5)
                fireball.dead = True
                
                if self.player.health == 0:
                    self.on_game_over()
                    
            if fireball.dead:
                self.projectiles.remove(fireball)
                
    def render(self, surface, offset_x=0, offset_y=0):
        super().render(surface, offset_x, offset_y)
        for fireball in self.projectiles:
            fireball.render(surface)