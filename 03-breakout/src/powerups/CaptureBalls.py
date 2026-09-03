import random
from typing import TypeVar

from gale.factory import Factory

import settings
from src.Ball import Ball
from src.powerups.PowerUp import PowerUp

class CaptureBalls(PowerUp):
    def __init__(self, x: int, y: int):
        super().__init__(x, y, 10)
        
    def take(self, play_state: TypeVar("PlayState")) -> None:

        play_state.powerup_active = True
        self.active = False
        
        
        