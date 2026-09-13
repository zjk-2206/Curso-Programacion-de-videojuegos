from typing import Any, TypeVar

import pygame

from gale.state import StateMachine
from gale.timer import Timer

import settings
from src.Projectile import Projectile
from src.states.entity.BaseEntityState import BaseEntityState
from src.states.entity.movement import move_and_bump


class PlayerTakeRow(BaseEntityState):
    def __init__(
        self,
        player: TypeVar("Player"),
        state_machine: StateMachine,
        dungeon: TypeVar("Dungeon"),
    ) -> None:
        super().__init__(player, state_machine)
        self.dungeon = dungeon

    def enter(self) -> None:
        player = self.entity 
        player.change_animation("port-row")
        Timer.after(1.0, lambda: player.change_state("idle"))
        
    def update(self, dt: float) -> None:
        pass
    
    def render(self, surface: pygame.Surface) -> None:
        anim = self.entity.current_animation
        self.entity.render_sprite(surface, anim.texture_id, anim.get_current_frame())
        
