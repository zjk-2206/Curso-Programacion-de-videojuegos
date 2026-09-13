import pygame

import settings
from typing  import TypeVar

from src.states.entity.BaseEntityState import BaseEntityState
from gale.state import StateMachine
from src.definitions.game_objects import GAME_OBJECT_DEFS
from src.GameObject import GameObject
from src.Projectile import Projectile


class PlayerShootState(BaseEntityState):
    def __init__(
        self,
        player: TypeVar("Player"),
        state_machine: StateMachine,
        dungeon: TypeVar("Dungeon"),
    ) -> None:
        super().__init__(player, state_machine)
        self.dungeon = dungeon
        self.entity.change_animation(f"shoot-{self.entity.direction}")

    def enter(self):
        pass

    def update(self, dt: float):
        self.entity.interact_requested = False
        
        if self.entity.row_requested:
            self.entity.row_requested = False
            
            arrow = GameObject(GAME_OBJECT_DEFS["arrow"], self.entity.x, self.entity.y)
            arrow.state = self.entity.direction
            self.dungeon.current_room.projectiles.append(
                Projectile(arrow, self.entity.direction)
            )
            self.entity.change_state("idle")
            return
            

    def render(self, surface: pygame.Surface):
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())