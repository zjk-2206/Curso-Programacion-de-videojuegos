import random
import settings
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp

class BombUp(PowerUp):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 6)
        
    def take(self, play_state: TypeVar("PlayState")) -> None:
        brickset = play_state.brickset
        
        for brick in brickset.bricks.items():
            brick[1].hit()
        
        settings.SOUNDS["boom"].play()
        settings.SOUNDS["boom"].set_volume(0.8)
        self.active = False
        